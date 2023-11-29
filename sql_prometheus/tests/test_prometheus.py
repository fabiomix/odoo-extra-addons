# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestPrometheus(TransactionCase):

    def setUp(self):
        super(TestPrometheus, self).setUp()
        self.PrometheusQuery = self.env['prometheus.query']
        self.ResUsers = self.env['res.users']
        active_users_sql = """
            SELECT COALESCE(ru.active, false) AS active, COUNT(ru.id) AS value
            FROM res_users ru WHERE true
            GROUP BY COALESCE(ru.active, false)
            ORDER BY COALESCE(ru.active, false);
        """
        self.active_users_metric = self.PrometheusQuery.create({
            'name': 'Active Users',
            'metric_name': 'active_users_test',
            'metric_type': 'gauge',
            'value_column': 'value',
            'code': active_users_sql
        })

    def test_01_metadata(self):
        data = self.active_users_metric.get_metric_data()
        self.assertEqual(len(data), 4)  # metadata x2, active=false, active=true
        self.assertEqual(data[0], '# HELP active_users_test Active Users.')
        self.assertEqual(data[1], '# TYPE active_users_test gauge')

    def test_02_active_users(self):
        data = self.active_users_metric.get_metric_data()
        active_users = self.ResUsers.search_count([])
        self.assertEqual(data[3], 'active_users_test{active="True"} %s' % (active_users))

    def test_03_sql_prohibited_words(self):
        self.assertRaises(
            ValidationError,
            self.active_users_metric.write,
            {'code': "TRUNCATE TABLE prometheus_query;"}
        )

    def test_04_value_column(self):
        self.active_users_metric.write({'value_column': 'fake_column'})
        self.assertRaises(
            KeyError,
            self.active_users_metric._get_metric_values,
        )
