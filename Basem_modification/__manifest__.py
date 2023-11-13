
{
    'name': 'Basem Product ',
    'version': '1.0',
    'category': 'Employees',
    'summary': """ custom Product """,
    'description': """custom  Product""",
    'author': 'Basem walid',
    'depends': ['base', 'hr','product'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_inherit_view.xml',
        'views/product_template_inherit_view.xml'
    ],
    'qweb': [],
    'license': 'LGPL-3',
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
