from odoo import models, fields, api
from pprint import pprint

class WizardStockPickingGenerator(models.TransientModel):
    _name= 'wizard.stock.picking.generator'
    _description = 'Generador de ordenes de entrega'
    
    awd_sale_id = fields.Many2one('sale.order', string='Orden de venta')
    # awd_stock_picking = fields.Many2many('')

    @api.model
    def default_get(self, fields):
        rec = super(WizardStockPickingGenerator, self).default_get(fields)
        id_ctx = self.env.context.get('active_id', False)
        rec['awd_sale_id'] = id_ctx
        return rec

    def compute_picking_generator(self):
        # for record in self:
        for record in self:
            print(record.awd_sale_id)
            sale = record.awd_sale_id
            warehouses = self.env['stock.warehouse'].search([('company_id', '=', self.env.company.id)])
            print(warehouses)
            for warehouse in warehouses:
                if warehouse == sale.warehouse_id:
                    print('ACTUAL', warehouse.name)
                    picking_current = self._make_stock_picking_order(sale, warehouse)
                else:
                    picking_other = self._make_stock_picking_order(sale, warehouse)
                    print('OTHER', warehouse.name)


            prices = []
            for line in sale.order_line:
                prices.append(int(line.awd_price_selector))
                qty_current = 0
                if 'CU' in warehouse.code:
                    qty_current += line.awd_stocks
                if 'NA' in warehouse.code:
                    qty_current += line.awd_stocks1

                qty_final =  qty_current - line.product_uom_qty
                qty_residue = line.product_uom_qty - qty_current
                qty_order = 0
                # print("PRODUCTO", line.name)
                # print("PRODUCTO", line.name)
                # print("ACTUAL STOCK", qty_current)
                # print("COMPRADO", qty_final)
                if qty_residue > 0:
                    qty_order = line.product_uom_qty - qty_residue
                else:
                    qty_order = line.product_uom_qty
                if qty_final < 0:
                    print("ORDEN: Necesitamos otra orden", qty_order)
                    # pprint(picking_current)
                    self._make_line_stock_move(line, picking_current, qty_order)
                    if qty_residue > 0:
                        print("ORDEN RESIDUAL", qty_residue)
                        # pprint(picking_other)
                        self._make_line_stock_move(line, picking_other, qty_residue)
                if qty_final >= 0:
                    print("ORDEN: No necesitamos otra orden", qty_order)
                    # pprint(picking_current)
                    self._make_line_stock_move(line, picking_current, qty_order)

            picking_current.sale_id = sale.id
            picking_other.sale_id = sale.id

            if sale.awd_partner_cat != '3':
                if 3 in prices or 4 in prices:
                    sale.state = 'to_approve'
                    return {'type': 'ir.actions.client', 'tag': 'reload'}
                else:
                    sale.state = 'sale'
                    return {'type': 'ir.actions.client', 'tag': 'reload'}
            else:
                if 4 in prices:
                    print(record.state)
                    record.state = 'to_approve'
                    return {'type': 'ir.actions.client', 'tag': 'reload'}
                else:
                    sale.state = 'sale'
                    return {'type': 'ir.actions.client', 'tag': 'reload'}

        return True


    def _make_stock_picking_order(self, sale, warehouse):
        locations = self.env['stock.location'].search([
                            ('usage', '=', 'customer')
                        ], limit=1)
        values = {
                "picking_type_id": warehouse.out_type_id.id ,
                "partner_id": sale.partner_id.id,
                "location_id": warehouse.lot_stock_id.id,
                "location_dest_id" : locations.id,
                "sale_id" : sale.id,
                "origin": sale.name,
                "scheduled_date": sale.create_date,
                }
        # print(values)
        stock_picking = self.env['stock.picking'].create(values)
        return stock_picking

    def _make_line_stock_move(self, line, picking, quantity):
        product = self.env['product.product'].search([
                            ('product_tmpl_id', '=', line.product_template_id.id )
                        ], limit=1)
        values = {
            'name': product.display_name,
            'product_id': product.id,
            'product_uom_qty': quantity,
            'product_uom': line.product_uom.id,
            'picking_id': picking.id,
            "location_id": picking.location_id.id,
            "location_dest_id" : picking.location_dest_id.id,
            "origin": picking.origin,
            "picking_type_id": picking.picking_type_id.id,
            # "picking_type_id": picking['picking_type_id'],
            # "location_id": picking['location_id'],
            # "location_dest_id" : picking['location_dest_id'],
            # "origin": picking['origin'],
            'picking_code': 'outgoing',

        }
        # picking.move_ids_without_packages.create(values)
        self.env['stock.move'].create(values)
        return True