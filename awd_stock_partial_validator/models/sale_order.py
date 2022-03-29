from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        for record in self:
            lines = self.env['sale.order.line'].search([
                            ('order_id', '=', record.id)
                        ])
            for line in lines:
                if ((float(line.awd_stocks) + float(line.awd_stocks1)) < float(line.product_uom_qty) ):
                    raise UserError(_("ALGUNO DE TUS PRODUCTOS NO ESTA DISPONIBLE EN STOCK, REVISA TU COTIZACIÓN"))
                if (float(line.product_uom_qty) == 0):
                    raise UserError(_("NO PUEDES PEDIR STOCK VACIO"))    
                if(float(line.product_uom_qty) > float(line.awd_stocks) or float(line.product_uom_qty) > float(line.awd_stocks1) and float(line.awd_stocks1) != 0 and float(line.awd_stocks) !=0   ):
                    wizard_form = self.env.ref('awd_stock_partial_validator.awd_wizard_stock_move_view_form', False)
                    view_id = self.env['awd.wizard.stock.move']
                    # vals = {
                    #         'name'   : 'this is for set name',
                    #     }
                    # new = view_id.create(vals)
                    return {
                            'name'      : _('Ordenes de entrega de stock parciales'),
                            'type'      : 'ir.actions.act_window',
                            'res_model' : 'awd.wizard.stock.move',
                            'res_id'    : view_id.id,
                            'view_id'   : wizard_form.id,
                            'view_type' : 'form',
                            'view_mode' : 'form',
                            'target'    : 'new'
                        }
                    # pass
                else:
                    res = super(SaleOrder, self).action_confirm()
                    return res