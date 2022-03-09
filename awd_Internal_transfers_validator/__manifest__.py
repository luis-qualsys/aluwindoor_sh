{
    'name': 'AWD - Validador de transferencias internas',
    'version': '15.0.1',
    'summary': 'Validador de transferencias internas para módulo de inventario',
    'description': '''
        Validador de transferencias internas para módulo de inventario
        Adición 4 de precios a productos para poder elegir en ventas
        
        Uso de password para validar una transferencia
    ''',
    'category': 'Inventory',
    'author': "Qualsys Consulting",
    'website': "http://www.qualsys.com.mx",
    'license': 'LGPL-3',
    'depends': [
        'stock',
        'sale'
    ],
    'data': [
        'security/security.xml',
        
        'views/stock_picking_inherit_views.xml',
    ],
    'installable': True,
    'application': True,
}
