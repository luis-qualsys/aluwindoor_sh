from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('to_approve', 'Por aprobar')])

    def action_confirm(self):
        for record in self:
            prices = []
            print('Clasificación', record.awd_partner_cat)
            for line in record.order_line:
                prices.append(int(line.awd_price_selector))
            if prices != []:
                prices.sort(reverse=True)
                print(prices)
                if record.awd_partner_cat != '3':
                    if 3 in prices or 4 in prices:
                        record.state = 'to_approve'
                        return {'type': 'ir.actions.client', 'tag': 'reload'}
                    else:
                        res = super(SaleOrder, self).action_confirm()
                        return res
                else:
                    if 4 in prices:
                        print(record.state)
                        record.state = 'to_approve'
                        return {'type': 'ir.actions.client', 'tag': 'reload'}
                    else:
                        res = super(SaleOrder, self).action_confirm()
                        return res
            else:
                raise UserError(_('No se pueden aprobar productos sin lista de precio configurada.'))


    def action_approval(self):
        for record in self:
            super(SaleOrder, self).action_confirm()

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    awd_price_selector = fields.Selection(string="Lista de precios", selection=[
        ('1', 'Precio 1'),
        ('2', 'Precio 2'),
        ('3', 'Precio 3'),
        ('4', 'Precio 4')
        ], default='1')

    @api.depends('product_template_id')
    @api.onchange("awd_price_selector")
    def _onchange_price_unit(self):
        for record in self:
            if record.awd_price_selector == '2':
                record.price_unit = record.product_template_id.awd_list_price2
            elif record.awd_price_selector == '3':
                record.price_unit = record.product_template_id.awd_list_price3
            elif record.awd_price_selector == '4':
                record.price_unit = record.product_template_id.awd_list_price4
            else:
                record.price_unit = record.product_template_id.list_price