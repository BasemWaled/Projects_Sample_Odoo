# -*- coding: utf-8 -*-
{
    'name': 'Owl Javascript app_one',
    'version': '1.0',
    'category': 'OWL',
    'author': 'BaSeM_WaLiD',
    'summary': 'Learning OWL Javascript',
    'sequence': -1,
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # Add OWL JS files here if needed
            'app_one/static/src/components/listView/listView.css',
            'app_one/static/src/components/listView/listView.js',
            'app_one/static/src/components/listView/listView.xml',
        ],
    },
    'application': True,
    'installable': True,
    'auto_install': False,
}