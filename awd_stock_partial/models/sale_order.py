from curses import resize_term
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order.line'
    
    awd_stocks = fields.Integer(string ='Stock Cuajimalpa', compute="stockwh")
    awd_stocks1 = fields.Integer(string ='Stock Naucalpan', compute="stockwh")
    
    @api.depends('product_template_id')
    @api.onchange('product_template_id')
    def stockwh(self): 
        for record in self:
            awd_ware= {}
            lst = []
            stock_quant = self.env['stock.quant'].search([
            ('product_id', '=', record.product_template_id.name),
            ])
            # print('Location', stock_quant)
            if len(stock_quant):
                for stock in stock_quant:
                    awd_ware[stock.location_id.display_name]= float(stock.quantity)
                for key in awd_ware.keys():
                    if 'NA' in key:
                        record.awd_stocks =  awd_ware[key]
                    if 'CU' in key:
                        record.awd_stocks1 =  awd_ware[key]
            else:
                record.awd_stocks = 0
                record.awd_stocks1 = 0

    @api.onchange('product_template_id', 'product_uom_qty')
    def onchange_stock(self):
        for record in self: 
            # print(record.product_template_id.property_stock_inventory)
            # if record.product_template_id != False:
            if record.product_template_id.id != 0:
                if record.product_template_id.qty_available < record.product_uom_qty:
                    return{
                            'warning': {
                            'title': "Advertencia:",
                            'message': "NO HAY SUFICIENTES PRODUCTOS DISPONIBLES EN EL ALMACEN ELEGIDO",
                        
                        }}