from xml.dom import ValidationErr

from odoo import models, fields, api, _
from odoo.tools import format_amount
from datetime import date
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class StockTransform(models.Model):
    _name = 'stock.transform'

    # awd_sucursal = fields.Many2one("crm.team",string="Sucursal")
    name = fields.Char(string='Nombre',readonly=True,required=True,copy=False,default="New")
    awd_product = fields.Many2one('product.product','Producto original', required=True)
    awd_location_origin = fields.Many2one('stock.location','Ubicación Origen', required=True)
    awd_transform_qty = fields.Integer('Cantidad a transformar', required=True)
    awd_product_result = fields.Many2one('product.product','Producto resultado', required=True)
    awd_location_destination = fields.Many2one('stock.location','Ubicación Destino', required=True,compute="_setting_location")
    awd_transformed_qty = fields.Integer('Cantidad resultante', required=True)
    awd_apply_date = fields.Date('Fecha de aplicación')
    state = fields.Selection(string='Estado', 
                            selection=[('pending', 'Pendiente'),
                                        ('done', 'Procesado')], default='pending')
    company_id=fields.Many2one('res.company','Compañía',default=lambda self: self.env['res.company'].browse(self.env['res.company']._company_default_get('stock.transform')))

    @api.depends('awd_location_origin')
    def _setting_location(self):
        for record in self:
            record.awd_location_destination=record.awd_location_origin

    def stock_transforming(self):
        print(self)
        total=0
        quant_id=0
        for quant in self.awd_location_origin.quant_ids:
            print(quant.product_id)
            print(self.awd_product)
            print(self.awd_product.id)
            if quant.product_id.id==self.awd_product.id:
                total=total+quant.quantity
                quant_id=quant.id
        if self.awd_transform_qty <= 0:
            raise ValidationError("La cantidad a transformar debe contener al menos una unidad.")
        if self.awd_transformed_qty <= 0:
            raise ValidationError("La cantidad resultante debe contener al menos una unidad.")
        if total < self.awd_transform_qty:
            raise ValidationError("La cantidad de productos a transformar es menor a la cantidad en este almacén. Cantidad: %s Almacén: %s" % (total,self.awd_location_origin.name))
        vals={
            'product_id' : self.awd_product.id,
            'quantity' : total,
            'inventory_quantity' : (total-self.awd_transform_qty),
            'inventory_diff_quantity' : -self.awd_transform_qty,
            'location_id' : self.awd_location_origin.id,
            'awd_transformation' : True,
            # 'company_id' : self.awd_location_origin.company_id.id,
        }
        if total==0:
            self.env["stock.quant"].create(vals)
        else:
            updated_quant = self.env["stock.quant"].search([('id', '=', quant_id)])
            updated_quant.write(vals)

        total=0
        quant2_id=0
        for quant in self.awd_location_destination.quant_ids:
            if quant.product_id.id==self.awd_product_result.id:
                quant2_id=quant.id
                total=total+quant.quantity
        vals={
            'product_id' : self.awd_product_result.id,
            'quantity' : total,
            'inventory_quantity' : total + self.awd_transformed_qty,
            'inventory_diff_quantity' : self.awd_transformed_qty,
            'location_id' : self.awd_location_destination.id,
            'awd_transformation' : True,
            # 'company_id' : self.awd_location_origin.company_id.id,
        }
        print("vals 2")
        print(vals)
        if total==0:
            self.env["stock.quant"].create(vals)
        else:
            updated_quant2=self.env["stock.quant"].search([('id', '=', quant2_id)])
            updated_quant2.write(vals)
        self.state="done"
        self.awd_apply_date=date.today()
            
    @api.model
    def create(self, vals):
        if vals.get('name','New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('product.transformation.code') or 'New'
            # number = self.env['ir.sequence'].get('product.transformation.code') or ''
            # res.write({'name': number})
            print("nombre:")
            print(vals['name'])
        res = super(StockTransform, self).create(vals)
        return res


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    awd_transformation = fields.Boolean('¿Viene de transformación?',default=False)

    @api.model
    def create(self,vals):
        print("create")
        print(self)
        print(vals)
        res = super().create(vals)
        print(res)
        if res.awd_transformation:
            print("if transformation")
            res.action_apply_inventory()
            # res.with_context({'inventory_report_mode': False}).action_apply_inventory()
        return res

    def write(self,vals):
        print("write")
        print(self)
        print(vals)
        res = super().write(vals)
        print(res)
        #print(self.awd_transformation)
        #print('in_date' not in vals)
        # if self.awd_transformation==True and 'in_date' not in vals and 'inventory_date' not in vals:
        if "awd_transformation" in vals: 
            print("transformation or q_set")
            self.with_context({'inventory_report_mode': False}).action_apply_inventory()
        # if res and self.env.context.get('inventory_report_mode'):
        #     # update context to prevent recursive write call
        #     self.with_context({'inventory_report_mode': False}).action_apply_inventory()
        return res

    # def action_apply_inventory(self):
    #     products_tracked_without_lot = []
    #     for quant in self:
    #         rounding = quant.product_uom_id.rounding
    #         if fields.Float.is_zero(quant.inventory_diff_quantity, precision_rounding=rounding)\
    #                 and fields.Float.is_zero(quant.inventory_quantity, precision_rounding=rounding)\
    #                 and fields.Float.is_zero(quant.quantity, precision_rounding=rounding):
    #             continue
    #         if quant.product_id.tracking in ['lot', 'serial'] and\
    #                 not quant.lot_id and quant.inventory_quantity != quant.quantity:
    #             products_tracked_without_lot.append(quant.product_id.id)
    #     # for some reason if multi-record, env.context doesn't pass to wizards...
    #     ctx = dict(self.env.context or {})
    #     ctx['default_quant_ids'] = self.ids
    #     quants_outdated = self.filtered(lambda quant: quant.is_outdated)
    #     if quants_outdated:
    #         ctx['default_quant_to_fix_ids'] = quants_outdated.ids
    #         return {
    #             'name': _('Conflict in Inventory Adjustment'),
    #             'type': 'ir.actions.act_window',
    #             'view_mode': 'form',
    #             'views': [(False, 'form')],
    #             'res_model': 'stock.inventory.conflict',
    #             'target': 'new',
    #             'context': ctx,
    #         }
    #     if products_tracked_without_lot:
    #         ctx['default_product_ids'] = products_tracked_without_lot
    #         return {
    #             'name': _('Tracked Products in Inventory Adjustment'),
    #             'type': 'ir.actions.act_window',
    #             'view_mode': 'form',
    #             'views': [(False, 'form')],
    #             'res_model': 'stock.track.confirmation',
    #             'target': 'new',
    #             'context': ctx,
    #         }
    #     print("_apply")
    #     print(self)
    #     self._apply_inventory()
    #     self.inventory_quantity_set = False

    # def _apply_inventory(self):
    #     print("_apply1")
    #     move_vals = []
    #     if not self.user_has_groups('stock.group_stock_manager'):
    #         raise UserError(_('Only a stock manager can validate an inventory adjustment.'))
    #     print("_apply2")
    #     for quant in self:
    #         # Create and validate a move so that the quant matches its `inventory_quantity`.
    #         if float_compare(quant.inventory_diff_quantity, 0, precision_rounding=quant.product_uom_id.rounding) > 0:
    #             move_vals.append(
    #                 quant._get_inventory_move_values(quant.inventory_diff_quantity,
    #                                                  quant.product_id.with_company(quant.company_id).property_stock_inventory,
    #                                                  quant.location_id))
    #         else:
    #             move_vals.append(
    #                 quant._get_inventory_move_values(-quant.inventory_diff_quantity,
    #                                                  quant.location_id,
    #                                                  quant.product_id.with_company(quant.company_id).property_stock_inventory,
    #                                                  out=True))
    #     print("_apply3")
    #     moves = self.env['stock.move'].with_context(inventory_mode=False).create(move_vals)
    #     print("_apply4")
    #     moves._action_done()
    #     print("_apply5")
    #     self.location_id.write({'last_inventory_date': fields.Date.today()})
    #     date_by_location = {loc: loc._get_next_inventory_date() for loc in self.mapped('location_id')}
    #     for quant in self:
    #         quant.inventory_date = date_by_location[quant.location_id]
    #     self.write({'inventory_quantity': 0, 'user_id': False})
    #     self.write({'inventory_diff_quantity': 0})

    #Se sobreescribio _apply_inventory con elfin de que se muestre si el movimiento del producto 
    #viene desde una transformación de produto o no
    def _apply_inventory(self):
        move_vals = []
        if not self.user_has_groups('stock.group_stock_manager'):
            raise UserError(_('Only a stock manager can validate an inventory adjustment.'))
        for quant in self:
            # Create and validate a move so that the quant matches its `inventory_quantity`.
            if float_compare(quant.inventory_diff_quantity, 0, precision_rounding=quant.product_uom_id.rounding) > 0:
                move_vals.append(
                    quant._get_inventory_move_values(quant.inventory_diff_quantity,
                                                     quant.product_id.with_company(quant.company_id).property_stock_inventory,
                                                     quant.location_id))
            else:
                move_vals.append(
                    quant._get_inventory_move_values(-quant.inventory_diff_quantity,
                                                     quant.location_id,
                                                     quant.product_id.with_company(quant.company_id).property_stock_inventory,
                                                     out=True))
            
            move_vals[0]['awd_transformation'] = True
        moves = self.env['stock.move'].with_context(inventory_mode=False).create(move_vals)
        moves._action_done()
        self.location_id.write({'last_inventory_date': fields.Date.today()})
        date_by_location = {loc: loc._get_next_inventory_date() for loc in self.mapped('location_id')}
        for quant in self:
            quant.inventory_date = date_by_location[quant.location_id]
        self.write({'inventory_quantity': 0, 'user_id': False})
        self.write({'inventory_diff_quantity': 0})


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    #awd_etiqueta = fields.Char(string='Origen de movimiento')
    awd_transformation = fields.Boolean('¿Viene de transformación?',default=False, compute='_get_origin')

    @api.depends('move_id')
    def _get_origin(self):
        for record in self:
            record.awd_transformation = record.move_id.awd_transformation

    @api.model_create_multi
    def create(self, vals_list):
        print("stock.move.line create")
        res = super(StockMoveLine,self).create(vals_list)
        return res

    def write(self,vals):
        print("stock.move.line write")
        res = super(StockMoveLine,self).write(vals)
        return res

    def _action_done(self):
        print("stock.move.line action_done")
        res = super(StockMoveLine,self)._action_done()
        return res

#toma el valor si el producto viene de transformación o no y lo muestra
class StockMove(models.Model):
    _inherit = 'stock.move'
    
    awd_transformation = fields.Boolean('¿Viene de transformación?',default=False)
