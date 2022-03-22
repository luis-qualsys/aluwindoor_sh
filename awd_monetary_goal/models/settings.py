from ast import Store
from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta

class SalesGoalsSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    date_default= date.today()
    awd_sales_goals_period = fields.Integer(string='Dias de periodo', default= 15)
    awd_sales_goals_date_init= fields.Date(string='Inicio de periodo',  inverse="_inverse_init_date", default=date.today(), store= True)
    awd_sales_goals_date_end= fields.Date(string='Fin de periodo', compute= "get_date_end", store= True)
    awd_monetary_goal_price1= fields.Float(string='Lista 1' , store= True)
    awd_monetary_goal_price2= fields.Float(string='Lista 2' , store= True)
    awd_monetary_goal_price3= fields.Float(string='Lista 3' , store= True)
    awd_monetary_goal_price4= fields.Float(string='Lista 4' , store= True)
        
    
    
    
        
    @api.depends("awd_sales_goals_date_end")   
    def get_new_date_init(self) :
        
        
            for record in self :
                
                record.awd_sales_goals_date_init = record.awd_sales_goals_date_end - relativedelta(days= record.awd_sales_goals_period)
                
        
        
        
    def _inverse_init_date(self):
        for record in self:
            
            if record.awd_sales_goals_date_end == date.today():
                record.awd_sales_goals_date_init = date.today() + relativedelta(days= 1)
            else : 
                record.awd_sales_goals_date_init = record.awd_sales_goals_date_init 
    @api.depends("awd_sales_goals_period", "awd_sales_goals_date_init")
    def get_date_end(self) : 
        for record in self :
            
            record.awd_sales_goals_date_end = record.awd_sales_goals_date_init + relativedelta(days= record.awd_sales_goals_period)


    def set_values(self):
        res = super(SalesGoalsSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('awd_monetary_goal.awd_sales_goals_period', self.awd_sales_goals_period)
        self.env['ir.config_parameter'].set_param('awd_monetary_goal.awd_sales_goals_date_init', self.awd_sales_goals_date_init)
        self.env['ir.config_parameter'].set_param('awd_monetary_goal.awd_sales_goals_date_end', self.awd_sales_goals_date_end)
        self.env['ir.config_parameter'].set_param('awd_monetary_goal.awd_monetary_goal_price1', self.awd_monetary_goal_price1)
        self.env['ir.config_parameter'].set_param('awd_monetary_goal.awd_monetary_goal_price2', self.awd_monetary_goal_price2)
        self.env['ir.config_parameter'].set_param('awd_monetary_goal.awd_monetary_goal_price3', self.awd_monetary_goal_price3)
        self.env['ir.config_parameter'].set_param('awd_monetary_goal.awd_monetary_goal_price4', self.awd_monetary_goal_price4)
        return res

    @api.model
    def get_values(self):
        res = super(SalesGoalsSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        awd_sales_goals_period = ICPSudo.get_param('awd_monetary_goal.awd_sales_goals_period')
        awd_sales_goals_date_init = ICPSudo.get_param('awd_monetary_goal.awd_sales_goals_date_init')
        awd_sales_goals_date_end = ICPSudo.get_param('awd_monetary_goal.awd_sales_goals_date_end')
        awd_monetary_goal_price1 = ICPSudo.get_param('awd_monetary_goal.awd_monetary_goal_price1')
        awd_monetary_goal_price2 = ICPSudo.get_param('awd_monetary_goal.awd_monetary_goal_price2')
        awd_monetary_goal_price3 = ICPSudo.get_param('awd_monetary_goal.awd_monetary_goal_price3')
        awd_monetary_goal_price4 = ICPSudo.get_param('awd_monetary_goal.awd_monetary_goal_price4')
        res.update(
            awd_sales_goals_period = awd_sales_goals_period,
            awd_sales_goals_date_init = awd_sales_goals_date_init,
            awd_sales_goals_date_end = awd_sales_goals_date_end,
            awd_monetary_goal_price1 = awd_monetary_goal_price1,
            awd_monetary_goal_price2 = awd_monetary_goal_price2,
            awd_monetary_goal_price3 = awd_monetary_goal_price3,
            awd_monetary_goal_price4 = awd_monetary_goal_price4
            
            
        )

        return res
