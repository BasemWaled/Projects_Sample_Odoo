# -*- coding: utf-8 -*-
{
    'name': 'Alboraq Dashboard',
    'version': '1.0',
    'category': 'OWL',
    'author': 'BaSeM_WaLiD',
    'summary': 'Learning OWL Javascript',
    'sequence': -1,
    'depends': ['base', 'web', 'sale', 'board'],
    'data': [
        'views/sales_dashboard.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'basem_dash/static/src/js/dashboard.js',
            'basem_dash/static/src/xml/dashboard.xml',
            'basem_dash/static/src/css/**/*.css',
        ],
    },
    'application': True,
    'installable': True,
}
