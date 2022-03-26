from statistics import quantiles
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError

class WizardHrEmployeeGetGoals(models.TransientModel):
    _name = 'wizard.hr.employee.get.goals'
    _description = 'Obtener metas monetarias empleados'

    name = fields.Char(string='Meta')

    awd_date_init = fields.Date(string="Fecha de inicio")
    awd_date_end = fields.Date(string="Fecha de termino")
    hr_employee_id = fields.Many2one('hr.employee', string="Empleado")

    @api.model
    def default_get(self, fields):
        rec = super(WizardHrEmployeeGetGoals, self).default_get(fields)
        id_ctx = self.env.context.get('active_id', False)
        rec['hr_employee_id'] = id_ctx
        return rec

    def get_goals_employee(self):
        for record in self:
            if record.hr_employee_id.crm_team_id.id:
                computed = 0.0
                values = {
                    'name': f'Periodo {record.awd_date_init} - {record.awd_date_end}',
                    'employee_id': record.hr_employee_id.id,
                    'awd_employee_goal': record.hr_employee_id.crm_team_id.awd_monetary_goal,
                }
                price1, price2, price3, price4 = record.get_parametters()
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
                if record.hr_employee_id.awd_is_vendor:
                    orders = self.env['sale.order'].search([
                        ('user_id', '=', record.hr_employee_id.user_id.id),
                        ('date_order', '>=', record.awd_date_init),
                        ('date_order', '<=', record.awd_date_end),
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
                        ('date_order', '>=', record.awd_date_init),
                        ('date_order', '<=', record.awd_date_end),
                        ('state', '=', "sale"),
                        ('team_id', '=', record.hr_employee_id.crm_team_id.id)
                        ])
                    for order in orders:
                        computed += order.amount_total

                if computed >= values['awd_employee_goal']:
                    values['state'] = 'done'
                else:
                    values['state'] = 'fail'

                values['awd_comision'] = sum(commissions.values())
                record.hr_employee_id.awd_hist_employee_goals_ids.create(values)

                return {'type': 'ir.actions.client', 'tag': 'reload'}

            else:
                raise UserError(_("Necesitas configurar el equipo de ventas."))


    def get_parametters(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        awd_monetary_goal_price1 = float(ICPSudo.get_param('awd_monetary_goals.awd_goal_price1'))/100
        awd_monetary_goal_price2 = float(ICPSudo.get_param('awd_monetary_goals.awd_goal_price2'))/100
        awd_monetary_goal_price3 = float(ICPSudo.get_param('awd_monetary_goals.awd_goal_price3'))/100
        awd_monetary_goal_price4 = float(ICPSudo.get_param('awd_monetary_goals.awd_goal_price4'))/100

        return awd_monetary_goal_price1, awd_monetary_goal_price2, awd_monetary_goal_price3, awd_monetary_goal_price4