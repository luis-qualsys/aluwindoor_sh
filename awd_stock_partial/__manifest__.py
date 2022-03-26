{
    'name': 'AWD - Stock en cotizaciones',
    'version': '15.0.1',
    'summary': 'Agrega el stock de inventario en las cotizaciones de venta',
    'description': '''
        
        Adicióna de columna de stock en ordenes de venta
        
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
        'views/sale_order_inherit_views.xml',
        
    ],
    'installable': True,
    'application': True,
}
