{
    'name': 'AWD - Actualización de datos de factura',
    'version': '15.0.1',
    'summary': 'Carga automatica de valores de Factura a partir de ficha de cliente',
    'description': '''
Adición de campos en Ficha de Partner 
- Forma de pago
- Uso de factura

Las facturas no podrán ser modificada más que por un usuario con los permisos suficientes.
    ''',
    'category': 'Account',
    'author': "Qualsys Consulting",
    'website': "http://www.qualsys.com.mx",
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'l10n_mx_edi',
    ],
    'data': [
        'views/res_partner_inherit_views.xml',
        'views/account_move_inherit_views.xml',
    ],
    'installable': True,
    'application': True,
}
