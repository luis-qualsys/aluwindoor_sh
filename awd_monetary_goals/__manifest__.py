{
    'name': 'AWD - Meta monetaria por sucursal',
    'version': '15.0.1',
    'summary': 'Asiganción de metas monetarias por sucursales',
    'description': '''
        Asigan meta monetaria por equipo de ventas y asigna las comiciones de los vendedores y el equipo operativo
    ''',
    'category': 'Sales',
    'author': "Qualsys Consulting",
    'website': "http://www.qualsys.com.mx",
    'license': 'LGPL-3',
    'depends': [
        'base',
        'sale',
        'hr' ,
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizards/wizard_crm_team_get_goals.xml',
        'views/crm_team_inherit_views.xml',
        'views/settings.xml',
        'data/ir_cron.xml',
    ],
    'installable': True,
    'application': True,
}
