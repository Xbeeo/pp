# -*- coding: utf-8 -*-
{
    "name": "Prime Plastic Report",

    'version': '19.0.0.0',

    'summary': """Prime Plastic Report""",

    'description': """Prime Plastic Report""",

    'category': 'all',

    'author': "SelectaSol",

    'website': 'https://selectasol.com',

    "depends": ['base', 'stock', 'mrp', 'prime_plastic_custom'],

    "data": [
        'security/ir.model.access.csv',
        'wizard/product_stock_report_wizard.xml',
        'wizard/production_item_ledger_views.xml',
        'report/action_report.xml',
        'report/product_stock_report_template.xml',
        'report/gate_pass_report.xml',
        'report/payment_receipt_report.xml',
        'report/partner_ledger_report.xml',
        'report/aged_partner_balance.xml',
        'report/production_item_ledger_report.xml',
        'views/partner_balance_menus.xml',

    ],

    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}
