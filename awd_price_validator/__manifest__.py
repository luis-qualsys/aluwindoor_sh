{
    'name': 'AWD - Validador de precios',
    'version': '15.0.1',
    'summary': 'Validador de precios 3 y 4 para módulo de ventas',
    'description': '''
        Validador de precios para módulo de ventas
        Adición 4 de precios a productos para poder elegir en ventas
        Validador de precios para productos 3 y 4
        Uso de password para validar una venta
    ''',
    'category': 'Sales',
    'author': "Qualsys Consulting",
    'website': "http://www.qualsys.com.mx",
    'license': 'LGPL-3',
    'depends': [
        'base',
        'stock',
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/product_template_inherit_views.xml',
        'views/sale_order_inherit_views.xml',
        'views/purchase_order_inherit_views.xml',
        'views/awd_product_family_views.xml',
    ],
    'installable': True,
    'application': True,
}
