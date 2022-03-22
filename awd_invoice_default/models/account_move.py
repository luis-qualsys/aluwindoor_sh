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