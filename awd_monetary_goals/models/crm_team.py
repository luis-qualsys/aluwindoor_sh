from odoo import models, fields, api
from datetime import date

class CrmTeam(models.Model):
    _inherit = 'crm.team'
    
    awd_monetary_goal = fields.Float(string='Meta monetaria', default=0.0)
    awd_hist_goals_ids = fields.One2many('awd.crm.team.goals', 'sale_team_id', string='Metas Historico')

    def get_goal_team(self):
        teams = self.env['crm.team'].search([])
        print(teams)
        for team in teams:
            sales_total = 0
            values = {}
            date_init, date_end = self.get_date_cron()
            if len(team.member_ids) >= 1:
                for member in team.member_ids:
                    orders = self.env['sale.order'].search([
                                                ('user_id', '=', member.id),
                                                ('date_order', '>=', date_init), 
                                                ('date_order', '<=', date_end),
                                                ('state', '=', "sale")
                                                ])
                    for order in orders:
                        sales_total += order.amount_total
            else:
                continue

            if  sales_total >=  team.awd_monetary_goal:
                values['state'] = "done"
            else :
                values['state'] = "fail"

            values['awd_sales_qty'] = sales_total
            values['name'] = f"Meta {date_init} - {date_end}"
            values['sale_team_id'] = team.id
            values['awd_period_init'] = date_end
            values['awd_period_end'] = date_end
            values['awd_goals'] = team.awd_monetary_goal
            values['awd_sales_qty'] = sales_total
            values['awd_origin_aut'] = True

            print(values)
            
            # team.crm_team_id.awd_hist_goals_ids.create(values)

        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def get_date_cron(self):
        date_end = date.today()
        date_init = date(date_end.year, date_end.month, 1)
        return date_init, date_end