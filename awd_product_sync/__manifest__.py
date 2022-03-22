{
    'name': 'AWD - Actualizador de productos para cotizaciones',
    'version': '15.0.1',
    'summary': 'Módul opara actualizar los precios de los productos en ordenes de venta',
    'description': '''
        Creación de función para actualizar los precios de productos una vez cambiados en la ficha de productos
        Función se carga una vez cargada la vista de formulario
    ''',
    'category': 'Account',
    'author': "Qualsys Consulting",
    'website': "http://www.qualsys.com.mx",
    'license': 'LGPL-3',
    'depends': [
        'base',
        'sale',
        'awd_price_validator'
    ],
    'data': [
        # 'views/sale_order_inherit_views.xml',
    ],
    'installable': True,
    'application': True,
}
