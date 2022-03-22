from odoo import models, api, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def read(self, fields=None, load='_classic_read'):
        if 'order_line' in fields:
            for record in self:
                if record.state == 'draft':
                    for order_line in record.order_line:
                        if order_line.awd_price_selector == '2':
                            print("Precio 2: actualizado")
                            order_line.price_unit = order_line.product_template_id.awd_list_price2
                        elif order_line.awd_price_selector == '3':
                            print("Precio 3: actualizado")
                            order_line.price_unit = order_line.product_template_id.awd_list_price3
                        elif order_line.awd_price_selector == '4':
                            print("Precio 4: actualizado")
                            order_line.price_unit = order_line.product_template_id.awd_list_price4
                        else:
                            print("Precio 1: actualizado")
                            order_line.price_unit = order_line.product_template_id.list_price

        res=super(SaleOrder,self).read(fields,load)
        return res
