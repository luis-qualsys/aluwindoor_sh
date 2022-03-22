from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    awd_partner_cat = fields.Selection(string='Clasificación de Cliente', related='partner_id.awd_category', store=True)
    # awd_partner_cat = fields.Selection(string='Clasificación de Cliente', selection=[
    #                                     ('0', 'Ninguno'),
    #                                     ('1', 'Bronce'),
    #                                     ('2', 'Plata'),
    #                                     ('3', 'Oro')
    #                                 ], compute='_get_categories')

    # @api.depends('partner_id')
    # def _get_categories(self):
    #     for record in self:
    #         if record.partner_id:
    #             record.awd_partner_cat = record.partner_id.awd_category
    #         else:
    #             record.awd_partner_cat = '0'

# class StockMove(models.Model):
#     _inherit = 'stock.move'
#     awd_family_product = fields.Char(string='Familia', related='product_id.awd_product_family_id.name')

class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'
    awd_family_product = fields.Char(string='Familia', related='product_id.awd_product_family_id.name', store=True)

class StockQuant(models.Model):
    _inherit = 'stock.quant'
    awd_family_product = fields.Char(string='Familia', related='product_id.awd_product_family_id.name', store=True)