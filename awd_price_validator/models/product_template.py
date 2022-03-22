from odoo import models, fields, api, _
from odoo.tools import format_amount
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    awd_list_price2 = fields.Float('Precio de venta 2', default=0.0)
    awd_list_price3 = fields.Float('Precio de venta 3', default=0.0)
    awd_list_price4 = fields.Float('Precio de venta 4', default=0.0)

    awd_tax_string2 = fields.Char(compute='_compute_tax_string2')
    awd_tax_string3 = fields.Char(compute='_compute_tax_string3')
    awd_tax_string4 = fields.Char(compute='_compute_tax_string4')

    awd_product_family_id = fields.Many2one('awd.product.family',
                                        string='Familia de producto')


    @api.constrains('awd_list_price2')
    def _check_list_price_one(self):
        for record in self:
            if record.list_price:
                if not (record.list_price > record.awd_list_price2):
                    raise ValidationError(_('La cantidad de la lista de precio 2 debe ser menor a la lista de precio 1'))

    @api.constrains('awd_list_price3')
    def _check_list_price_two(self):
        for record in self:
            if record.list_price:
                if not (record.awd_list_price2 > record.awd_list_price3):
                    raise ValidationError(_('La cantidad de la lista de precio 3 debe ser menor a la lista de precio 2'))

    @api.constrains('awd_list_price4')
    def _check_list_price_three(self):
        for record in self:
            if record.list_price:
                if not (record.awd_list_price3 > record.awd_list_price4):
                    raise ValidationError(_('La cantidad de la lista de precio 4 debe ser menor a la lista de precio 3'))

    @api.depends('taxes_id', 'awd_list_price2')
    def _compute_tax_string2(self):
        for record in self:
            currency = record.currency_id
            res = record.taxes_id.compute_all(record.awd_list_price2)
            joined = []
            included = res['total_included']
            if currency.compare_amounts(included, record.awd_list_price2):
                joined.append(_('%s Incl. Taxes', format_amount(self.env, included, currency)))
            excluded = res['total_excluded']
            if currency.compare_amounts(excluded, record.awd_list_price2):
                joined.append(_('%s Excl. Taxes', format_amount(self.env, excluded, currency)))
            if joined:
                record.awd_tax_string2 = f"(= {', '.join(joined)})"
            else:
                record.awd_tax_string2 = " "

    def _compute_tax_string3(self):
        for record in self:
            currency = record.currency_id
            res = record.taxes_id.compute_all(record.awd_list_price3)
            joined = []
            included = res['total_included']
            if currency.compare_amounts(included, record.awd_list_price3):
                joined.append(_('%s Incl. Taxes', format_amount(self.env, included, currency)))
            excluded = res['total_excluded']
            if currency.compare_amounts(excluded, record.awd_list_price3):
                joined.append(_('%s Excl. Taxes', format_amount(self.env, excluded, currency)))
            if joined:
                record.awd_tax_string3 = f"(= {', '.join(joined)})"
            else:
                record.awd_tax_string3 = " "

    def _compute_tax_string4(self):
        for record in self:
            currency = record.currency_id
            res = record.taxes_id.compute_all(record.awd_list_price4)
            joined = []
            included = res['total_included']
            if currency.compare_amounts(included, record.awd_list_price4):
                joined.append(_('%s Incl. Taxes', format_amount(self.env, included, currency)))
            excluded = res['total_excluded']
            if currency.compare_amounts(excluded, record.awd_list_price4):
                joined.append(_('%s Excl. Taxes', format_amount(self.env, excluded, currency)))
            if joined:
                record.awd_tax_string4 = f"(= {', '.join(joined)})"
            else:
                record.awd_tax_string4 = " "


class ProductCategory(models.Model):
    _inherit = 'product.category'

    company_id = fields.Many2one(comodel_name='res.company', string='Compañia')