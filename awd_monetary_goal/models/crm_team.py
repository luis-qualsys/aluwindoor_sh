from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class CrmTeam(models.Model):
    _inherit = 'crm.team'
    
    awd_period_init = fields.Date(string='Inicio de periodo')
    awd_period_end= fields.Date(string='Fin de periodo')
    awd_monetary_goal = fields.Float(string='Meta monetaria', default=0.0)
    awd_hist_goals_ids = fields.One2many('awd.crm.team.goals', 'sale_team_id', string='Metas Historico')
    
    def dummy(self):
        
        
        orders = self.env['sale.order'].search([
        ('date_order', '>=', self.awd_period_init), 
        ('date_order', '<=', self.awd_period_end),
        ('amount_total', '>', 0),
        ('state', '=', "sale"),
        ('name', '!=', " "),
        ])
        
        sales_total=0.0
        for order in orders: 
            print(order)
            if order.state == "sale":
                
                sales_total += order.amount_total
            
        if  sales_total >=  self.awd_monetary_goal:
            status = "done"
        else :
            status = "fail"
        
        

        vals={
        'name': f"Meta {self.awd_period_init} - {self.awd_period_end}",
        'sale_team_id': self.id,
        'awd_period_init1': self.awd_period_init,
        'awd_period_end1': self.awd_period_end,
        'awd_goals':  self.awd_monetary_goal,
        'awd_sales_qty' : sales_total,
        'state' : status,
        'awd_process' : 'Manual',
        'company_id'  : self.company_id.id
        }
        self.awd_hist_goals_ids.create (vals)
        employ_search= self.env['hr.employee'].search([
            ("awd_crm_team_id", "=", self.id),
        ])
        
        # for employee in employ_search : 
                
        #     employee.manual()
            

    def btn_p(self):
        button= self.env['res.config.settings'].sudo()
        for butn in button:
            butn.execute()
        
        sett = self.env['ir.config_parameter'].sudo()
        

        awd_sales_goals_date_init = sett.get_param('awd_monetary_goal.awd_sales_goals_date_init')
        
        awd_sales_goals_date_end=sett.get_param('awd_monetary_goal.awd_sales_goals_date_end')
        
        
        
        ids= self.env['crm.team'].search([
            ("company_id", "=", 1),
            
        ])
        for i_d in ids :
            
        
            orders = self.env['sale.order'].search([
            ('team_id', '=', i_d.id),
            ('date_order', '>=', awd_sales_goals_date_init), 
            ('date_order', '<=', awd_sales_goals_date_end),
            ('amount_total', '>', 0),
            ('state', '=', "sale"),
            ('name', '!=', " "),
            ])
            
            
            sales_total=0.0
            for order in orders: 
                if order.state == "sale":
                    
                    sales_total += order.amount_total
                
            if  sales_total >=  i_d.awd_monetary_goal:
                status = "done"
            else :
                status = "fail"
        
            

            
            valos={
            'name': f"Meta {awd_sales_goals_date_init} - {awd_sales_goals_date_end}",
            'sale_team_id': i_d.id,
            'awd_period_init1': awd_sales_goals_date_init,
            'awd_period_end1': awd_sales_goals_date_end,
            'awd_goals':  i_d.awd_monetary_goal,
            'awd_sales_qty' : sales_total,
            'state' : status,
            'awd_process' : 'Automatico',
            'company_id'  : i_d.company_id.id
            }
            i_d.awd_hist_goals_ids.create (valos)
            

        employ_search= self.env['hr.employee'].search([])
        
        for employee in employ_search : 
                
            employee.goals()
            


