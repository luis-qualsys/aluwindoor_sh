from string import printable
from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    awd_salary = fields.Float(string="Salario" , default= 0.0)
    
    awd_hist_employee_goals_ids = fields.One2many('awd.hr.employee.goal', 'employee_id', string='Metas de empleado')
    awd_crm_team_id= fields.Many2one ('crm.team', string ='equipo de ventas')
    
    
    

    
    


    def goals(self):
        
        
        sett = self.env['ir.config_parameter'].sudo()

        awd_sales_goals_date_init = sett.get_param('awd_monetary_goal.awd_sales_goals_date_init')
        
        awd_sales_goals_date_end=sett.get_param('awd_monetary_goal.awd_sales_goals_date_end')
        awd_monetary_goal_price1=float(sett.get_param('awd_monetary_goal.awd_monetary_goal_price1'))/100
        awd_monetary_goal_price2=float(sett.get_param('awd_monetary_goal.awd_monetary_goal_price2'))/100
        awd_monetary_goal_price3=float(sett.get_param('awd_monetary_goal.awd_monetary_goal_price3'))/100
        awd_monetary_goal_price4=float(sett.get_param('awd_monetary_goal.awd_monetary_goal_price4'))/100
        
        comision= 0.0
        com_amount1 = 0.0
        com_amount2 = 0.0
        com_amount3 = 0.0
        com_amount4 = 0.0
        
        sales_total=0.0
        price_1_count= 0.0
        price_2_count= 0.0
        price_3_count= 0.0
        price_4_count= 0.0
        goal= self.env['crm.team'].search([
            ("company_id", "=", 1),
            ("id", "=", self.awd_crm_team_id.id),
        ])
        
        
        

        
        
        for his in goal :
            
            
            orders_sale = self.env['sale.order'].search([
            ('team_id', '=', his.id),
            ('date_order', '>=', awd_sales_goals_date_init), 
            ('date_order', '<=', awd_sales_goals_date_end),
            ('amount_total', '>', 0),
            ('state', '=', "sale"),
            ('name', '!=', " "),
            ])
            
            
            
            
            
            for order in orders_sale: 
                if order.state == "sale":
                    
                    sales_total += order.amount_total
                    order_lines = self.env['sale.order.line'].search([
                        ("order_id", "=", order.id)
                    ])
                    if order.user_id != False :
                        for ord_line in order_lines : 
                            # print ("###########################",self.user_id.name, order.user_id.name)
                            # print ("########################################",self.id, order.user_id.id, order.state, ord_line.awd_price_selector)
                            if order.user_id.name == self.name and  ord_line.awd_price_selector == "1" :
                                
                                com_amount1= com_amount1 + (order.amount_total * awd_monetary_goal_price1)
                                price_1_count += order.amount_total
                            if order.user_id.name == self.name  and ord_line.awd_price_selector == "2" :
                                
                                com_amount2=com_amount2 +(order.amount_total * awd_monetary_goal_price2)
                                price_2_count += order.amount_total
                            if order.user_id.name == self.name and ord_line.awd_price_selector == "3" :
                                
                                com_amount3=com_amount3 +(order.amount_total * awd_monetary_goal_price3)
                                price_3_count += order.amount_total
                            if order.user_id.name == self.name and ord_line.awd_price_selector == "4" :
                                
                                com_amount4=com_amount4 + (order.amount_total * awd_monetary_goal_price4)
                                price_4_count += order.amount_total
                
            com_amount_total= com_amount1 + com_amount2 + com_amount3 + com_amount4
                    
                    
                    
            
            if  sales_total >=  his.awd_monetary_goal:
                status = "done"
            else :
                status = "fail"
            
            
            if self.job_id.name == "Vendedor" :
            
                if  sales_total >=  his.awd_monetary_goal: 
                        comision= com_amount_total
                        status = "logrado"
                else :
                        comision = 0.0
                        status = "No logrado"
            else : 
                if  sales_total >=  his.awd_monetary_goal: 
                        comision= 0.0
                        status = "logrado"
                else :
                        comision = 0.0
                        status = "No logrado"
                
                    

            
            
                
            val={
                    'employee_id' : self.id,
                    'goal_period':  f"Meta {awd_sales_goals_date_init} - {awd_sales_goals_date_end}",
                    'awd_employee_goal' : his.awd_monetary_goal,
                    'states' : status,
                    'salary_com': comision,
                    'list_1' : price_1_count,
                    'list_2' : price_2_count,
                    'list_3' : price_3_count,
                    'list_4' : price_4_count,
                    
            }
            
            self.awd_hist_employee_goals_ids.create (val)
            print("Datos de empleado", self.id ,  "guardados con exito")
            
    # def manual(self):
            
            
            
    #         comision= 0.0
            
    #         sales_total=0.0
    #         goal= self.env['crm.team'].search([
    #             ("company_id", "=", 1),
    #             ("id", "=", self.awd_crm_team_id.id),
    #         ])
            
            
            
            
            
    #         for his in goal :
                
                
    #             order_sale = self.env['sale.order'].search([
    #             ('team_id', '=', his.id),
    #             ('date_order', '>=', his.awd_period_init), 
    #             ('date_order', '<=', his.awd_period_end),
    #             ('amount_total', '>', 0),
    #             ('state', '=', "sale"),
    #             ('name', '!=', " "),
    #             ])
                
                
                
    #             for order in order_sale: 
    #                 if order.state == "sale":
                        
    #                     sales_total += order.amount_total
                    
    #             if  sales_total >=  his.awd_monetary_goal:
    #                 status = "done"
    #             else :
    #                 status = "fail"
                
    #             if self.job_id.name == "Vendedor" :
                
    #                 if  sales_total >=  his.awd_monetary_goal: 
    #                         comision= sales_total * 0.01
    #                         status = "logrado"
    #                 else :
    #                         comision = 0.0
    #                         status = "No logrado"
    #             else : 
    #                 if  sales_total >=  his.awd_monetary_goal: 
    #                         comision= self.awd_salary/4
    #                         status = "logrado"
    #                 else :
    #                         comision = 0.0
    #                         status = "No logrado"
                    
                        

                
                
                    
    #             valmanual={
    #                     'employee_id' : self.id,
    #                     'goal_period':  f"Meta {his.awd_period_init} - {his.awd_period_end}",
    #                     'awd_employee_goal' : his.awd_monetary_goal,
    #                     'states' : status,
    #                     'salary' : self.awd_salary,
    #                     'salary_com': comision,
    #                     'process'   : 'Manual',
    #             }
                
    #             self.awd_hist_employee_goals_ids.create (valmanual)
    #             print("Datos de empleado", self.id ,  "guardados con exito")

