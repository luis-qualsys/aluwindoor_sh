{
    'name': 'AWD - Revisión de Stock Ventas',
    'version': '15.0.1',
    'summary': 'Adición de Información de WH en cotizaciones de venta',
    'description': '''
        Adicióna de columna de stock en ordenes de venta
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
        'views/sale_order_inherit_views.xml',
        'wizards/wizard_stock_picking_generator_views.xml',
    ],
    'installable': True,
    'application': True,
}
