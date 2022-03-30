from odoo import models, fields, api, _
from odoo.exceptions import UserError
class StockMove(models.Model):
    _inherit = 'stock.move'
    state = fields.Selection(selection_add=[('to_approve', 'Por aprobar')])

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    state = fields.Selection(selection_add=[('to_approve', 'Por aprobar')])

    def button_validate(self):
        for record in self:
            print(record.state)
            if len(record.move_line_ids_without_package) !=0:
                if record.picking_type_id.code == 'internal':
                    record.state = 'to_approve'
                    return {'type': 'ir.actions.client', 'tag': 'reload'}
                else:
                    res = super(StockPicking, self).button_validate()
                    return res
            else : 
                raise UserError(_('No se pueden aprobar transferencias internas vacias.'))

    def action_approval_stock(self):
        for record in self:
            if len(record.move_line_ids_without_package) !=0:
                print(len(record.move_line_ids_without_package))
                super(StockPicking, self).button_validate()
            else: 
                raise UserError(_('No se pueden aprobar transferencias internas vacias.'))

    def action_no_approval_stock(self):
        for record in self:
            record.state = 'draft'
            return {'type': 'ir.actions.client', 'tag': 'reload'}
