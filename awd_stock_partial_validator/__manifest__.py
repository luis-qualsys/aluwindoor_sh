{
    'name': 'AWD - Ordenes parciales Validador',
    'version': '15.0.1',
    'summary': 'Genera ordenes parciales dependiendo del stock',
    'description': '''
        Crea ordenes parciales dependiendo el stock de producto
    ''',
    'category': 'Sales',
    'author': "Qualsys Consulting",
    'website': "http://www.qualsys.com.mx",
    'license': 'LGPL-3',
    'depends': [
        'stock',
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/awd_wizard_stock_move.xml',
        # 'views/sale_order_inherit_views.xml',
    ],
    'installable': True,
    'application': True,
}
