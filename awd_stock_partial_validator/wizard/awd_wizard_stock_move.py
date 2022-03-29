from odoo import models, fields, api

class AwdWizardStockMove(models.TransientModel):
    _name= 'awd.wizard.stock.move'
    wiz_id= fields.Many2one('sale.order', string='id')

    @api.model
    def default_get(self, fields):
        rec = super(AwdWizardStockMove, self).default_get(fields)
        id_ctx = self.env.context.get('active_id', False)
        rec['wiz_id'] = id_ctx

        return rec

    def calculate (self):
            awd_stock_order= {}
            for record in self:
                print (record)
                s_order = self.env['sale.order'].search([
                    ('id', '=', record.wiz_id.id)
                ])
                print("//////////////",s_order)
                for order in s_order:
                    print(order.id)
                    lines = self.env['sale.order.line'].search([
                        ('order_id', '=', order.id)
                        
                    ] )
                    for line in lines:
                                stock_p = self.env['stock.warehouse'].search([
                                
                                ('company_id', '=', order.company_id.id)
                                ])
                                
                                for stock in stock_p:
                                        
                                    print(order.warehouse_id.id)
                                        
                                    if (order.warehouse_id.id == 1):
                                        qty_select= line.awd_stocks
                                        qty_other= line.awd_stocks1
                                    else:
                                        qty_select= line.awd_stocks1
                                        qty_other= line.awd_stocks
                                            # print("VALORES CREATE PARTE DE ARRIBA DE ORDEN",
                                            # "\npicking_type_id: ", stock.out_type_id ,
                                            # "\nPartner_id: ", order.partner_id,
                                            # "\nLocation_id: ", stock.out_type_id.default_location_src_id,
                                            # "\nlocation_dest_id: ", stock.out_type_id.default_location_dest_id,
                                            # "\norigin ", order.name,
                                            # "\nCREATE DE LINEAS"
                                            # "\nname: ", line.product_template_id,
                                            # "\nproduct_uom_qty: ", line.product_uom_qty,
                                            # "\nproduct_uom: ", line.product_uom,
                                            # "\nLocation_id: ", stock.out_type_id.default_location_src_id,
                                            # "\nlocation_dest_id: ", stock.out_type_id.default_location_dest_id,
                                            
                                            
                                            
                                            #             )
                                
                                #  Create incoming shipment.
                                # self.picking_in = self.env['stock.picking'].create({
                                #     'picking_type_id': self.picking_type_id,
                                #     'partner_id': self.partner_id,
                                #     'location_id': self.location_id,
                                #     'location_dest_id': self.location_dest_id,
                                # })
                                # self.env['stock.move'].create({
                                #     'name': self.product.name,
                                #     'product_id': self.product.id,
                                #     'product_uom_qty': 2,
                                #     'product_uom': self.product.uom_id.id,
                                #     'picking_id': self.picking_in.id,
                                #     'location_id': self.location_id,
                                #     'location_dest_id': self.location_dest_id})
                                    
                                        
                                    operation= float(line.product_uom_qty) - float(qty_select)
                                    
                                        
                                    
                                        
                                            
                                    print (line.product_uom_qty , line.awd_stocks )
                                            
                                    print("Almacen seleccionado: ", order.warehouse_id.name, "id:", order.warehouse_id.id  )
                                            
                                                
                                                
                                        
                                    print("/////////////////",stock.out_type_id.name)
                                                # for stck_p in stock_picking: 
                                                    
                                    print(stock.id)
                                    ubication= self.env['stock.location'].search([
                                                ("complete_name", "=", "Partner Locations/Customers")
                                            ])
                                                
                                        
                                    awd_stock_order= self.env['stock.picking'].create({
                                        "picking_type_id": stock.out_type_id.id ,
                                        "partner_id": order.partner_id.id,
                                        "location_id": stock.lot_stock_id.id,
                                        "location_dest_id" : ubication.id,
                                        "sale_id" : order.id,
                                        "origin": order.name,
                                        "scheduled_date": order.create_date,
                                        })
                                    
                                    if(float(line.product_uom_qty) > float(qty_select)):
                                        
                                                prod= self.env['product.product'].search([
                                                    ('product_tmpl_id', '=', line.product_template_id.id )
                                                    ],limit=1)
                                                self.env['stock.move'].create({
                                                'name': prod.name,
                                                'product_id': prod.id,
                                                'product_uom_qty': qty_select,
                                                'product_uom': 1,
                                                'picking_id': awd_stock_order.id,
                                                "location_id": stock.lot_stock_id.id,
                                                "location_dest_id" : ubication.id,
                                                "picking_type_id": stock.out_type_id.id ,
                                                'picking_code': 'outgoing',
                                                "origin": order.name, 
                                                
                                                })
                                    
                                                
                                    if(operation <= float(qty_other)):
                                                prod= self.env['product.product'].search([
                                                    ('product_tmpl_id', '=', line.product_template_id.id )
                                                    ],limit=1)
                                                self.env['stock.move'].create({
                                                'name': prod.name,
                                                'product_id': prod.id,
                                                'product_uom_qty': operation,
                                                'product_uom': 1,
                                                'picking_id': awd_stock_order.id,
                                                'picking_code': 'outgoing',
                                                "location_id": stock.lot_stock_id.id,
                                                "location_dest_id" : ubication.id,
                                                "picking_type_id": stock.out_type_id.id ,
                                                
                                                "origin": order.name,
                                                })
                                                print("SI IMPRIME PERO NO SE A DONDE LO MANDA")