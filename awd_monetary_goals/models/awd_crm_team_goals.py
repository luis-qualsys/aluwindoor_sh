from odoo import api, fields, models


class AwdCrmTeamGoals(models.Model):
    _name = 'awd.crm.team.goals'
    _description = 'Sale Team Goals'

    name = fields.Char(string='Meta')
    sale_team_id = fields.Many2one('crm.team', string='Equipo de ventas')
    # crm_team_id = fields.Integer(string='ID Ventas', related='sale_team_id.id')
    awd_period_init = fields.Date(string='Inicio de periodo')
    awd_period_end = fields.Date(string='Fin de periodo')
    awd_goals = fields.Float(string='Meta del periodo')
    awd_sales_qty = fields.Float('Cantidad vendida')
    state = fields.Selection(string='Estado', 
                            selection=[('fail', 'Fallido'),
                                        ('done', 'Logrado')], default='fail')
    awd_origin_aut = fields.Boolean(string='Automático', default=False)