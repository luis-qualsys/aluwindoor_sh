{
    'name': 'AWD - Meta monetaria por sucursal',
    'version': '15.0.1',
    'summary': 'Asiganción de metas monetarias por sucursales',
    'description': '''
        Asigan meta monetaria por equipo de ventas
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
        'views/crm_team_inherit_views.xml',
        'views/settings.xml',
        'views/hr_employee_inherit_views.xml',
        'data/ir_cron.xml',

    ],
    'installable': True,
    'application': True,
}
