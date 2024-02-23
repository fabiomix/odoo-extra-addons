{
    "name": "Kanban Modules Upgrade",
    "summary": "Shortcut to upgrade modules",
    "description": "Show the upgrade button in kanban when a module is installed.",
    "version": "12.0.1.0.0",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/OCA/OCB/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Technical Settings",
    "author": "fabiomix",
    "website": "https://github.com/fabiomix",
    "license": "AGPL-3",

    # any module necessary for this one to work correctly
    "depends": ['base'],

    "data": [
        'views/ir_module_module.xml',
    ],

    "application": False,
    "installable": True
}
