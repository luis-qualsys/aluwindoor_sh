from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    awd_partner_cat = fields.Selection(string='Categoria del Cliente',  related="partner_id.awd_category", store=True)