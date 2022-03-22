from odoo import api, fields, models


class AwdHrEmployeeGoal(models.Model):
    _name = 'awd.hr.employee.goal'
    _description = 'Employee Goals'

    
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    goal_period = fields.Char(string='Meta')
    awd_employee_goal = fields.Float(string='Meta del periodo' )
    states = fields.Char(string='Estado')
    salary = fields.Float(string='Salario')
    salary_com = fields.Float(string='Comision')
    process= fields.Char(string= "Calculo")
    origin = fields.Char(string='Origen', default='automatico')
    list_1 = fields.Float( string= 'Precio 1')
    list_2 = fields.Float( string= 'Precio 2')
    list_3 = fields.Float( string= 'Precio 3')
    list_4 = fields.Float( string= 'Precio 4')
