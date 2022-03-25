from string import printable
from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    awd_salary = fields.Float(string="Salario" , default= 0.0)
    
    awd_hist_employee_goals_ids = fields.One2many('awd.hr.employee.goal', 'employee_id', string='Metas de empleado')
    awd_crm_team_id= fields.Many2one ('crm.team', string ='equipo de ventas')

