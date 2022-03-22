from odoo import fields, models


class WizardCalculateGoalsTeam(models.TransientModel):
    _name = 'wizard.calculate.goals.team'
    _description = 'Wizard para calculo de metas'

    awd_date_init = fields.Date(string='Fecha de inicio')
    awd_date_end = fields.Date(string='Fecha de termino')
