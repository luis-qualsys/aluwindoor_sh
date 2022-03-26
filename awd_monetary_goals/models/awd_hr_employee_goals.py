from odoo import api, fields, models


class AwdHrEmployeeGoals(models.Model):
    _name = 'awd.hr.employee.goals'
    _description = 'Metas de empleado'

    name = fields.Char(string='Meta')
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    awd_employee_goal = fields.Float(string='Meta del periodo')
    state = fields.Selection(string='Estado', 
                            selection=[('fail', 'Fallido'),
                                        ('done', 'Logrado')], default='fail')
    awd_comision = fields.Float(string='Comisión')
    awd_origin_aut = fields.Boolean(string='Origen', default=False)
    awd_sale_list_1 = fields.Float( string= 'Ventas Precio 1')
    awd_sale_list_2 = fields.Float( string= 'Ventas Precio 2')
    awd_sale_list_3 = fields.Float( string= 'Ventas Precio 3')
    awd_sale_list_4 = fields.Float( string= 'Ventas Precio 4')
    awd_comicion_list_1 = fields.Float( string= 'Comición Precio 1')
    awd_comicion_list_2 = fields.Float( string= 'Comición Precio 2')
    awd_comicion_list_3 = fields.Float( string= 'Comición Precio 3')
    awd_comicion_list_4 = fields.Float( string= 'Comición Precio 4')
    awd_period_end = fields.Date(string='Fecha de termino')