from odoo import models, fields, api
from datetime import date, datetime, timedelta

class CrmTeam(models.Model):
    _inherit = 'crm.team'
    
    awd_monetary_goal = fields.Float(string='Meta monetaria', default=0.0)
    awd_hist_goals_ids = fields.One2many('awd.crm.team.goals', 'sale_team_id', string='Metas Historico')

    def get_goal_team(self):
        teams = self.env['crm.team'].search([])
        for team in teams:
            checker, date_init, date_end = self.get_date_cron(team)
            sales_total = 0
            values = {}
            if checker:
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
                values['awd_period_init'] = date_init
                values['awd_period_end'] = date_end
                values['awd_goals'] = team.awd_monetary_goal
                values['awd_sales_qty'] = sales_total
                values['awd_origin_aut'] = True

                team.awd_hist_goals_ids.create(values)
            else:
                continue

        return True

    def get_date_cron(self, team):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        awd_date_init = ICPSudo.get_param('awd_monetary_goals.awd_sales_goals_date_init')
        today = date.today()
        if awd_date_init == None:
            return False, today, today
        date_init = awd_date_init.split('-') # yyyy mm yy
        date_initial = date(int(date_init[0]), int(date_init[1]), 1)
        goals = self.env['awd.crm.team.goals'].search([
                                ('sale_team_id', '=', team.id),
                                ('awd_origin_aut', '=', True)
                            ])
        if len(goals) > 0:
            dates = []
            for goal in goals:
                dates.append(goal.awd_period_end)
            dates.sort()
            last_date = dates[-1]
            print(last_date.month, today.month)
            if last_date.month == today.month and today.day in range(1,30):
                return False, today, today
            if last_date.month < today.month and last_date.month+1 != today.month:
                date_initial = date(last_date.year, last_date.month+1, 1)
                date_ended = date(date_initial.year, date_initial.month+1, 1) - timedelta(days=1)
                print(date_initial, date_ended)
                return True, date_initial, date_ended
            else:
                return False, today, today
        else:
            date_ended = date(date_initial.year, date_initial.month+1, 1) - timedelta(days=1)
            return True, date_initial, date_ended