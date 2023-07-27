# -*- coding: utf-8 -*-
{
    'name': "odoo_learn",

    'summary': """add botton to pos""",

    'description': """add botton to pos""",

    'author': "Basem Walid",
    'website': "https://www.techvano.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sales',
    'version': '16.0',
    'sequence': -100,
    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],

    # always loaded
    'data': [
        "views/views.xml",
    ],
    # only loaded in demonstration mode
    'assets': {
        'point_of_sale.assets': [
            "odoo_learn/static/src/js/wb_sample.js",
            "odoo_learn/static/src/js/hide_btn.js",
            "odoo_learn/static/src/xml/wb_sample.xml",
            "odoo_learn/static/src/xml/hide_btn.xml",
        ]
    }
}
