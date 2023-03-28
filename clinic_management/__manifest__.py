# -*- coding: utf-8 -*-
{
    'name': "clinic_management",
    'summary': """clinic_management""",
    'description': """clinic_management""",
    'author': "Basem Walid",
    'category': 'Uncategorized',
    'version': '1.0.0',
    'sequence': -100,
    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'account', 'product'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'wizard/medical_appointments_invoice_wizard.xml',
        'views/main_menu_file.xml',
        'views/appointment.xml',
        'views/patient.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3',
}
