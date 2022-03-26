from datetime import date, timedelta
from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    awd_hist_employee_goals_ids = fields.One2many('awd.hr.employee.goals', 'employee_id', string='Metas del empleado')
    crm_team_id= fields.Many2one ('crm.team', string ='Equipo de venta')
    awd_is_vendor = fields.Boolean(string='Es vendedor', default=False)

    def get_goals_employee(self):
        employees = self.env['hr.employee'].search([])
        for employee in employees:
            cheker, date_initial, date_ended = self.get_date_cron(employee)
            if cheker:
                if employee.crm_team_id.id:
                    computed = 0.0
                    values = {
                        'name': f'Periodo {date_initial} - {date_ended}',
                        'employee_id': employee.id,
                        'awd_employee_goal': employee.crm_team_id.awd_monetary_goal,
                        'awd_period_end': date_ended,
                        'awd_origin_aut': True
                    }
                    price1, price2, price3, price4 = self.get_parametters()
                    commissions = {
                        'awd_comicion_list_1': 0,
                        'awd_comicion_list_2': 0,
                        'awd_comicion_list_3': 0,
                        'awd_comicion_list_4': 0,
                    }
                    quantiles = {
                        'awd_sale_list_1': 0,
                        'awd_sale_list_2': 0,
                        'awd_sale_list_3': 0,
                        'awd_sale_list_4': 0,
                    }
                    if employee.awd_is_vendor:
                        orders = self.env['sale.order'].search([
                            ('user_id', '=', employee.user_id.id),
                            ('date_order', '>=', date_initial),
                            ('date_order', '<=', date_ended),
                            ('state', '=', "sale")
                            ])

                        for order in orders:
                            for line in order.order_line:
                                if line.awd_price_selector == "1" :
                                    commissions['awd_comicion_list_1'] += line.price_subtotal * price1
                                    quantiles['awd_sale_list_1'] += line.price_subtotal
                                if line.awd_price_selector == "2" :
                                    commissions['awd_comicion_list_2'] += line.price_subtotal * price2
                                    quantiles['awd_sale_list_2'] += line.price_subtotal 
                                if line.awd_price_selector == "3" :
                                    commissions['awd_comicion_list_3'] += line.price_subtotal * price3
                                    quantiles['awd_sale_list_3'] += line.price_subtotal
                                if line.awd_price_selector == "4" :
                                    commissions['awd_comicion_list_4'] += line.price_subtotal * price4
                                    quantiles['awd_sale_list_4'] += line.price_subtotal
                    else:
                        orders = self.env['sale.order'].search([
                            ('date_order', '>=', date_initial),
                            ('date_order', '<=', date_ended),
                            ('state', '=', "sale"),
                            ('team_id', '=', employee.crm_team_id.id)
                            ])
                        for order in orders:
                            computed += order.amount_total

                    if computed >= values['awd_employee_goal']:
                        values['state'] = 'done'
                    else:
                        values['state'] = 'fail'

                    values['awd_comision'] = sum(commissions.values())
                    print(values)
                    employee.awd_hist_employee_goals_ids.create(values)
                else:
                    continue
            else:
                continue
        return {'type': 'ir.actions.client', 'tag': 'reload'}


    def get_parametters(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        awd_monetary_goal_price1 = float(ICPSudo.get_param('awd_monetary_goals.awd_goal_price1'))/100
        awd_monetary_goal_price2 = float(ICPSudo.get_param('awd_monetary_goals.awd_goal_price2'))/100
        awd_monetary_goal_price3 = float(ICPSudo.get_param('awd_monetary_goals.awd_goal_price3'))/100
        awd_monetary_goal_price4 = float(ICPSudo.get_param('awd_monetary_goals.awd_goal_price4'))/100

        return awd_monetary_goal_price1, awd_monetary_goal_price2, awd_monetary_goal_price3, awd_monetary_goal_price4

    def get_date_cron(self, employee):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        awd_date_init = ICPSudo.get_param('awd_monetary_goals.awd_sales_goals_date_init')
        today = date.today()
        if awd_date_init == None:
            return False, today, today
        date_init = awd_date_init.split('-') # yyyy mm yy
        date_initial = date(int(date_init[0]), int(date_init[1]), 1)
        goals = self.env['awd.hr.employee.goals'].search([
                                ('employee_id', '=', employee.id),
                                ('awd_origin_aut', '=', True)
                            ])
        if len(goals) > 0:
            dates = []
            for goal in goals:
                dates.append(goal.awd_period_end)
            dates.sort()
            last_date = dates[-1]
            # print(last_date.month, today.month)
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
            # print(date_initial, date_ended)
            return True, date_initial, date_ended