# -*- coding: utf-8 -*-
{
    "name": "Rainbow theme",
    "summary": "Customize brand color",
    "description": "Customize the primary color of the Odoo Community theme.",
    "version": "14.0.1.0.0",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/OCA/OCB/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Themes/Backend",
    "author": "fabiomix",
    "website": "https://github.com/fabiomix",
    "license": "AGPL-3",

    # any module necessary for this one to work correctly
    "depends": ['web', 'base_setup'],

    "data": [
        'views/assets.xml',
        'views/res_config_settings.xml',
    ],

    "application": False,
    "installable": True
}
