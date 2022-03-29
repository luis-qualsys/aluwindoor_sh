from email.policy import default
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    awd_compute_monetary = fields.Boolean(string='Agregar a calculo de cómisiones', default=True)