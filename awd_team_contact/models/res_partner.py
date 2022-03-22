import unicodedata

from odoo import models, fields, api, _
from odoo.tools import format_amount
import logging
_logger = logging.getLogger(__name__)

def delete_accent(string):
    s = ''.join((c for c in unicodedata.normalize('NFD',string) if unicodedata.category(c) != 'Mn'))
    return s

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        # record = self.env['res.users'].search([('id', '=', self.env.uid)])
        # _logger.info("################################# res.partner  = %s",record.team_id)
        name = vals.get('name',False)
        if name:
            upper_name = delete_accent(name).upper()
            vals.update({'name':upper_name})

        # vals['user_id'] = self.env.uid
        # vals['awd_sucursal'] = record.team_id.id

        return super(ResPartner, self).create(vals)

    # def write(self, vals):
    #     vals['user_id'] = self.env.uid
    #     return super(ResPartner, self).write(vals)
