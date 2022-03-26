from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError

class WizardCrmTeamGetGoals(models.TransientModel):
    _name = 'wizard.crm.team.get.goals'
    _description = 'Obtener metas monetarias'

    awd_date_init = fields.Date(string="Fecha de inicio")
    awd_date_end = fields.Date(string="Fecha de termino")
    crm_team_id = fields.Many2one('crm.team', string="Equipo de ventas")

    @api.model
    def default_get(self, fields):
        rec = super(WizardCrmTeamGetGoals, self).default_get(fields)
        id_ctx = self.env.context.get('active_id', False)
        rec['crm_team_id'] = id_ctx
        return rec

    def get_goals_teams(self):
        for record in self:
            sales_total = 0
            values = {}
            if len(record.crm_team_id.member_ids) >= 1:
                for team in record.crm_team_id:
                    for member in team.member_ids:
                        orders = self.env['sale.order'].search([
                                                    ('user_id', '=', member.id),
                                                    ('date_order', '>=', record.awd_date_init), 
                                                    ('date_order', '<=', record.awd_date_end),
                                                    ('state', '=', "sale")
                                                    ])
                        for order in orders:
                            sales_total += order.amount_total
            else:
                raise UserError(_("Necesitas al menos un miembro en tu equipo de ventas."))

            if  sales_total >=  record.crm_team_id.awd_monetary_goal:
                values['state'] = "done"
            else :
                values['state'] = "fail"

            values['awd_sales_qty'] = sales_total
            values['name'] = f"Meta {record.awd_date_init} - {record.awd_date_end}"
            values['sale_team_id'] = record.crm_team_id.id
            values['awd_period_init'] = record.awd_date_init
            values['awd_period_end'] = record.awd_date_end
            values['awd_goals'] = record.crm_team_id.awd_monetary_goal
            values['awd_sales_qty'] = sales_total
            values['awd_origin_aut'] = False
            
            record.crm_team_id.awd_hist_goals_ids.create(values)

        return {'type': 'ir.actions.client', 'tag': 'reload'}