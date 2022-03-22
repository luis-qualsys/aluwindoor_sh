{
    'name': 'AWD - Segregación de contactos por vendedor',
    'version': '15.0.1',
    'summary': 'Separa los contactos para que sólo sean visibles por el vendedor que los crea',
    'description': '''
        Separa los contactos para que sólo sean visibles por el vendedor que los crea
    ''',
    'category': 'Sales',
    'author': "Qualsys Consulting",
    'website': "http://www.qualsys.com.mx",
    'license': 'LGPL-3',
    'depends': [
        'base',
        'contacts',
        'sale'
    ],
    'data': [
        'security/security.xml',
    ],
    'installable': True,
    'application': True,
}
