from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    awd_product_family_id = fields.Many2one('awd.product.family',
                                            string='Familia de producto')

class ProductCategory(models.Model):
    _inherit = 'product.category'

    company_id = fields.Many2one(comodel_name='res.company', string='Compañia')