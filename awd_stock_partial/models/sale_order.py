from curses import resize_term
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order.line'
    
    awd_stocks= fields.Char(string ='WHCU1', default="-", compute="stockwh")
    awd_stocks1= fields.Char(string ='WHNA1', default="-", compute="stockwh")
    awd_quantity_prod=fields.Float(string="cantidad")
    @api.depends('product_template_id')
    def stockwh(self): 
        # order= self.env['sale.order'].search([])
        # for orde in order:
        #     order_line= orde.order_line
        #     for orde in order_line:
                # product = self.env['product.template'].search([
                # ('id', '=', self.product_template_id.id),

                # ],limit=1)
                # for prod in product:
                awd_ware= {}
                lst = []
                for record in self:

                    stock = self.env['stock.quant'].search([
                    ('product_id', '=', record.product_template_id.name),
                    ])
                    sum_prod= 0.0
                    
                    for stck in stock :
                        # stocks = stck.location_id.name
                        sum_prod += float(stck.quantity)
                        
                        awd_ware[stck.location_id.display_name]= stck.quantity
                    
                    print("//////////////",sum_prod)
                    print("/////////////////////////",stock)
                    print("/////////////////////awd_ware",awd_ware)
                    res = ''
                    var = 0
                    var1= 0
                    for key in awd_ware.keys():
                        res += str(awd_ware[key]) 
                        
                        
                        lst.extend(awd_ware.values())
                        print(lst[0])
                        var = lst[0]
                        var1 = lst[2]
                        
                    record.awd_stocks= var
                    record.awd_stocks1= var1
                    # print(awd_ware['WHCU1/Existencias'])
    @api.onchange('product_template_id', 'product_uom_qty')
    
    def onchange_stock(self):
        for record in self: 
            # print(record.product_template_id.property_stock_inventory)
            # if record.product_template_id != False:
            if record.product_template_id.id != 0: 
                if record.product_template_id.qty_available < record.product_uom_qty:
                    print(record.product_template_id.qty_available)
                    print(record.product_uom_qty)        
                    return{
                            'warning': {
                            'title': "Advertencia:",
                            'message': "NO HAY SUFICIENTES PRODUCTOS DISPONIBLES EN EL ALMACEN ELEGIDO",
                        
                        }}
                    
                    
                    
