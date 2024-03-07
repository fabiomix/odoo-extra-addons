# -*- coding: utf-8 -*-
{
    "name": "Mail Delay Auto Delete",
    "summary": "Delay auto delete of sent email",
    "description": "Set a time retention policy for sent email.",
    "version": "10.0.1.0.0",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/OCA/OCB/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    "category": "Technical Settings",
    "author": "fabiomix",
    "website": "https://github.com/fabiomix",
    "license": "AGPL-3",

    # any module necessary for this one to work correctly
    "depends": ['mail'],

    "data": [
        'views/mail_mail.xml',
    ],

    "application": False,
    "installable": True
}
