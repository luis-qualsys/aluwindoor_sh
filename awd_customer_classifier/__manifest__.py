{
    'name': 'AWD - Clasificador de clientes',
    'version': '15.0.1',
    'summary': 'Clasificador de clientes basado en ventas',
    'description': '''
        Adición de catalogo de familias de productos
        Adición de información de clasificación de clientes 
    ''',
    'category': 'Stock',
    'author': "Qualsys Consulting",
    'website': "http://www.qualsys.com.mx",
    'license': 'LGPL-3',
    'depends': [
        'base',
        'stock',
        'sale',
        'awd_price_validator',
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'views/awd_product_family_views.xml',
        # 'views/product_template_inherit_views.xml',
        'views/res_partner_inherit_views.xml',
        'views/awd_res_partner_results_views.xml',
        'wizards/wizard_res_partner_classifier.xml',
        'views/settings.xml',
        'views/sale_order_inherit_form_views_2.xml',
        'views/sale_report_inherit.xml',
        'data/ir_cron.xml',
        'views/stock_reports_inherit.xml',
        'views/stock_picking_inherit_views.xml',
        'views/stock_quant_inherit_views.xml',
        'views/stock_valuation_layer_inherit_views.xml',
        'views/purchase_order_inherit_views.xml',
    ],
    # "assets": {
    #     "web.assets_backend": [
    #         "/awd_customer_classifier/static/src/js/awd_hide_button_box.js"
    #     ]},
    'installable': True,
    'application': True,
}
