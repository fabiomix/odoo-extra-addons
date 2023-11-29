# -*- coding: utf-8 -*-
from odoo import http

import logging
_logger = logging.getLogger(__name__)


class Prometheus(http.Controller):

    @http.route('/sql-prometheus/metrics', type='http', auth='none')
    def prometheus_metrics(self, **kw):
        metrics = http.request.env['prometheus.query'].sudo().search([])
        res = []
        for query in metrics:
            metric_data = query.get_metric_data()
            if metric_data is None:
                continue  # no data for this metric, skip
            res.extend(metric_data)
        # res is now something like [help, type, metric, metric, help, type, ...]
        response = http.request.make_response('\n'.join(res).encode('utf-8'))
        response.mimetype = "text/plain"
        return response
