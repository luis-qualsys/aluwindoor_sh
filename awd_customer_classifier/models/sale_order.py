from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    awd_partner_cat = fields.Selection(string='Categoria del Cliente', related="partner_id.awd_category", store=True)
    # compute='_get_categories',
    # @api.depends('partner_id')
    # def _get_categories(self):
    #     for record in self:
    #         if record.partner_id:
    #             record.awd_partner_cat = record.partner_id.awd_category
    #         else:
    #             record.awd_partner_cat = '0'
