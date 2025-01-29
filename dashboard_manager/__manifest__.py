# -*- coding: utf-8 -*-
{
    'name': 'Dashboard Manager',
    'version': '1.0',
    'category': 'Dashboard ',
    'author': 'BaSeM_WaLiD',
    'summary': '',
    'sequence': -1,
    'depends': ['base', 'web', 'sale', 'board', 'crm', 'account', 'purchase', 'portal'],
    'data': [
        'views/sales_dashboard.xml',
        'views/por_temp.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dashboard_manager/static/src/js/dashboard.js',
            'dashboard_manager/static/src/xml/dashboard.xml',
            'dashboard_manager/static/src/css/**/*.css',
        ],
    },
    'application': True,
    'installable': True,
}
