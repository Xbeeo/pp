# -*- coding: utf-8 -*-
{
    "name": "Prime Plastic Report",

    'version': '19.0.0.0',

    'summary': """Prime Plastic Report""",


    'description': """Prime Plastic Report""",

    'category': 'all',

    'author': "SelectaSol",

    'website': 'https://selectasol.com',

    "depends": ['base', 'stock','mrp','prime_plastic_custom'],

    "data": [
        'security/ir.model.access.csv',
        'wizard/product_stock_report_wizard.xml',
        'report/action_report.xml',
        'report/product_stock_report_template.xml',
        'report/gate_pass_report.xml',
        'report/payment_receipt_report.xml',
        'report/partner_ledger_report.xml',

    ],

    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}
