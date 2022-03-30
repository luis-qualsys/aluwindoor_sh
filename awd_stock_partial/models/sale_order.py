from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order.line'
    
    awd_stocks = fields.Integer(string ='Stock Cuajimalpa', compute="stockwh")
    awd_stocks1 = fields.Integer(string ='Stock Naucalpan', compute="stockwh")
    
    @api.depends('product_template_id')
    @api.onchange('product_uom_qty')
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
                        record.awd_stocks1 =  awd_ware[key] or 0
                    if 'CU' in key:
                        record.awd_stocks =  awd_ware[key] or 0
            else:
                record.awd_stocks = 0
                record.awd_stocks1 = 0

    @api.onchange('product_uom_qty')
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

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        for record in self:
            for line in record.order_line:
                if line.product_template_id.qty_available < line.product_uom_qty:
                    raise UserError(_("Alguno de tus productos no tiene suficiente Stock para tu entrega. Favor de revisar tu disponibilidad"))
                elif line.product_uom_qty == 0:
                    raise UserError(_("No puedes vender productos en cantidades de 0"))
                else:
                    warehouse = record.warehouse_id.lot_stock_id.display_name
                    if 'CU' in warehouse and line.product_uom_qty > line.awd_stocks:
                        print('OPEN WIZARD CUAJIMALPA')
                        # wizard_form = self.env.ref('awd_stock_partial.wizard_stock_picking_generator_form', False)
                        view_id = self.env['wizard.stock.picking.generator']
                        return {
                            'name'      : _('Generar ordenes de entrega parciales'),
                            'type'      : 'ir.actions.act_window',
                            'res_model' : 'wizard.stock.picking.generator',
                            'res_id'    : view_id.id,
                            # 'view_id'   : wizard_form.id,
                            'view_type' : 'form',
                            'view_mode' : 'form',
                            'target'    : 'new'
                        }
                    elif 'NA' in warehouse and line.product_uom_qty > line.awd_stocks1:
                        print('OPEN WIZARD NAUCALPAN')
                        # wizard_form = self.env.ref('awd_stock_partial.wizard_stock_picking_generator_form', False)
                        view_id = self.env['wizard.stock.picking.generator']
                        return {
                            'name'      : _('Generar ordenes de entrega parciales'),
                            'type'      : 'ir.actions.act_window',
                            'res_model' : 'awd.wizard.stock.move',
                            'res_id'    : view_id.id,
                            'view_type' : 'form',
                            'view_mode' : 'form',
                            'target'    : 'new'
                        }
                    else:
                        # print('Natural Action')
                        res = super(SaleOrder, self).action_confirm()
                        return res