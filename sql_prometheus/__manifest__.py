# -*- coding: utf-8 -*-
{
    "name": "SQL Prometheus",
    "summary": "Custom metrics from SQL",
    "description": "Define high-level application metrics for Prometheus using SQL query.",
    "version": "14.0.0.1.0",
    "development_status": "Beta",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/OCA/OCB/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Technical Settings",
    "author": "fabiomix",
    "website": "https://github.com/fabiomix",
    "license": "AGPL-3",

    # any module necessary for this one to work correctly
    "depends": ['base'],

    "data": [
        'views/prometheus_query.xml',
        'security/ir.model.access.csv',
    ],

    "demo": [
        'data/prometheus_query_demo.xml',
    ],

    "application": False,
    "installable": True
}
