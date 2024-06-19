# -*- coding: utf-8 -*-
{
    'name': 'Owl Javascript',
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
            'owl/static/src/components/**/*.js',
            'owl/static/src/components/**/*.xml',
            'owl/static/src/components/**/*.scss',
        ],
    },
    'application': True,
    'installable': True,
}
