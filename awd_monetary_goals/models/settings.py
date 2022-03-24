from ast import Store
from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta

class SalesGoalsSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    awd_sales_goals_date_init = fields.Date(string='Fecha de inicio')
    awd_goal_price1 = fields.Float(string='Lista 1')
    awd_goal_price2 = fields.Float(string='Lista 2')
    awd_goal_price3 = fields.Float(string='Lista 3')
    awd_goal_price4 = fields.Float(string='Lista 4')

    def set_values(self):
        res = super(SalesGoalsSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('awd_monetary_goals.awd_sales_goals_date_init', self.awd_sales_goals_date_init)
        self.env['ir.config_parameter'].set_param('awd_monetary_goals.awd_goal_price1', self.awd_goal_price1)
        self.env['ir.config_parameter'].set_param('awd_monetary_goals.awd_goal_price2', self.awd_goal_price2)
        self.env['ir.config_parameter'].set_param('awd_monetary_goals.awd_goal_price3', self.awd_goal_price3)
        self.env['ir.config_parameter'].set_param('awd_monetary_goals.awd_goal_price4', self.awd_goal_price4)
        return res

    @api.model
    def get_values(self):
        res = super(SalesGoalsSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        awd_sales_goals_date_init = ICPSudo.get_param('awd_monetary_goal.awd_sales_goals_date_init')
        awd_goal_price1 = ICPSudo.get_param('awd_monetary_goal.awd_goal_price1')
        awd_goal_price2 = ICPSudo.get_param('awd_monetary_goal.awd_goal_price2')
        awd_goal_price3 = ICPSudo.get_param('awd_monetary_goal.awd_goal_price3')
        awd_goal_price4 = ICPSudo.get_param('awd_monetary_goal.awd_goal_price4')
        res.update(
            awd_sales_goals_date_init = awd_sales_goals_date_init,
            awd_goal_price1 = awd_goal_price1,
            awd_goal_price2 = awd_goal_price2,
            awd_goal_price3 = awd_goal_price3,
            awd_goal_price4 = awd_goal_price4
        )

        return res
