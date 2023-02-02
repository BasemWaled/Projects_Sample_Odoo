# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'category': 'Hospital',
    'author': 'BaSeM_WaLiD',
    'sequence': -100,
    'summary': 'Hospital Management system',
    'description': """Hospital Management system""",
    'depends': ['base', 'mail', 'product', 'report_xlsx'],
    'data': ['security/ir.model.access.csv',
             'views/menu.xml',
             'views/patient_view.xml',
             'views/female_view.xml',
             'views/appointment_view.xml',
             'views/patient_tag.xml',
             'reports/report.xml',
             'reports/patient_card.xml'],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3',
}
