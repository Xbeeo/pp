# -*- coding: utf-8 -*-
{
    "name": "Prime Plastic Custom",

    'version': '19.0.0.0',

    'summary': """Prime Plastic Custom""",


    'description': """Prime Plastic Custom""",

    'category': 'all',

    'author': "SelectaSol",

    'website': 'https://selectasol.com',

    "depends": ['base', 'stock','product','sale','purchase','sale_stock'],

    "data": [
        'security/ir.model.access.csv',
        'views/colors_views.xml',
        'views/product_model_views.xml',
        'views/material_views.xml',
        'views/product_template_views.xml',
        'views/driver_name_views.xml',
        'views/vehicle_no_views.xml',
        'views/sale_order_view.xml',
        'views/stock_picking_view.xml',
        'views/account_payment_views.xml',
        'views/purchase_order_views.xml',
    ],

    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}
