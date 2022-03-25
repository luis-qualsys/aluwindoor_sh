from odoo import models, api, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id.awd_payment_methods:
            self.l10n_mx_edi_payment_method_id = self.partner_id.awd_payment_methods

        self.l10n_mx_edi_usage = self.partner_id.awd_usage_invoice

        res = super(AccountMove, self)._onchange_partner_id()

        return res

    def read(self, fields=None, load='_classic_read'):
        if 'partner_id' in fields:
            for record in self:
                if record.partner_id != None:
                    if self.partner_id.awd_payment_methods:
                        self.l10n_mx_edi_payment_method_id = self.partner_id.awd_payment_methods
                    self.l10n_mx_edi_usage = self.partner_id.awd_usage_invoice

        res= super(AccountMove,self).read(fields, load)
        return res
