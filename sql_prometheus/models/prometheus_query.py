# -*- coding: utf-8 -*-
import re

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

PROMETHEUS_METRIC_REGEX = '[a-zA-Z_:][a-zA-Z0-9_:]*'

SQL_PROHIBITED_WORDS = [
    "ALTER",
    "CREATE",
    "DELETE",
    "DROP",
    "EXECUTE",
    "INSERT",
    "TRUNCATE",
    "UPDATE",
]


class PrometheusQuery(models.Model):
    _name = 'prometheus.query'
    _description = 'Prometheus Metric Query'
    _rec_name = 'name'
    _order = 'name ASC'

    _sql_constraints = [
        ('unique_metric_name', 'unique(metric_name)', _('This metric name is already used.'))
    ]


    # Fields declaration

    name = fields.Char(
        string='Description',
        required=True,
        help='Description of the metric.'
    )

    metric_name = fields.Char(
        string='Metric name',
        required=True,
        copy=False,
        help='Name of the Prometheus metric.'
    )

    metric_type = fields.Selection(
        string='Metric type',
        selection=[('counter', 'Counter'), ('gauge', 'Gauge')],
        required=True,
        default='gauge'
    )

    value_column = fields.Char(
        string='Value column',
        required=True,
        help='Name of the column in query result that contains the metric value.'
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )

    code = fields.Text(
        string='SQL query',
        required=True,
        translate=False,
        help='SQL to extract the metric value.'
    )


    # Constraints and onchanges

    @api.constrains('metric_name')
    def _check_metric_name(self):
        pattern = re.compile(PROMETHEUS_METRIC_REGEX)
        for record in self:
            if not pattern.match(record.metric_name):
                raise ValidationError(_("Metric names may contain ASCII letters, digits and underscores."))

    @api.constrains('code')
    def _check_code(self):
        # [TODO] this constrain is NOT TOTALLY SAFE!
        for record in self:
            sql_query = record.code.upper().replace("\n", "")
            if any(bad_word in sql_query for bad_word in SQL_PROHIBITED_WORDS):
                raise ValidationError(_("Bad word found in query. Sure about that?"))


    # CRUD methods (and name_search, _search, ...) overrides

    def copy(self, default=None):
        default = default or {}
        metric_name = default.get('metric_name', False)
        if not metric_name:
            default.update({'metric_name': self.metric_name + _('_copy')})
        return super(PrometheusQuery, self).copy(default)


    # Action methods

    def action_test_query(self):
        for record in self:
            try:
                self.env.cr.execute(record.code)
                res = self.env.cr.dictfetchone()
            except Exception as ex:
                raise ValidationError(ex)
        return True


    # Business methods

    def _get_metric_labels(self, row):
        """
        Given a SQL result row in dict format, take every column/value pair
        and use them as Prometheus labels. Return as key=value csv string.
        """
        # return ','.join(f'{key}="{value}"' for key, value in row.items())
        return ','.join('{0}="{1}"'.format(key, value) for key, value in row.items())

    def _get_metric_values(self):
        """
        Run a single SQL metric query, return all the values as list
        of tuples, grouped by labels. Ex: [(metric_name, labels, value)]
        """
        self.env.cr.execute(self.code)
        query_results = self.env.cr.dictfetchall()
        res = []
        if not query_results:
            return res
        for row in query_results:
            value = row.pop(self.value_column)  # leave KeyError for bad config
            labels_str = self._get_metric_labels(row)
            res.append((self.metric_name, labels_str, value))
        return res

    def get_metric_data(self):
        """
        For the current metric, return metadata and query results as list of strings,
        following the Prometheus text format. Ex: [help, type, value_1, value_2]
        """
        self.ensure_one()
        data = self._get_metric_values()
        if not data:
            return None
        res = []
        res.append('# HELP {0} {1}.'.format(self.metric_name, self.name))
        res.append('# TYPE {0} {1}'.format(self.metric_name, self.metric_type))
        for metric_name, labels, value in data:
            # res.append(f'{metric_name}{{{labels}}} {value}')
            res.append('{0}{{{1}}} {2}'.format(metric_name, labels, value))
        return res
