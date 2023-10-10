# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'link_all_project',
    'version': '1.0.0',
    'category': 'Projects',
    'author': 'BaSeM_WaLiD',
    'sequence': -100,
    'summary': 'link_all_project',
    'description': """Link_all_Project_systems_and_admins_users""",
    'depends': ['base', 'mail', 'project'],
    'data': [
            'security/ir.model.access.csv',
            'views/links_view.xml',
            'views/project_view.xml',
        ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3',
}
