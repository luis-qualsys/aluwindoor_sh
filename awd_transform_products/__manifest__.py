{
    'name': 'AWD - Transformación de materiales',
    'version': '15.0.1',
    'summary': 'Transformador de productos a materiales',
    'description': '''
        Solo toma un producto y lo transforma en otro o otros
        Hace los cambios sobre el mismo Almacen
        Realiza el ajuste de inventario de los materiales convertidos
    ''',
    'category': 'Stock',
    'author': "Qualsys Consulting",
    'website': "http://www.qualsys.com.mx",
    'license': 'LGPL-3',
    'depends': [
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'views/product_template_inherit_views.xml',
        'views/transform_product_view.xml',
        'views/sequence_transform.xml',
        'views/stock_move_line_inherit_views.xml',
    ],
    'installable': True,
    'application': True,
}
