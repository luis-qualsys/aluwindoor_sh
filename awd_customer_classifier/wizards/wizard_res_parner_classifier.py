from odoo import fields, models


class WizardResPartnerClassifierMan(models.TransientModel):
    _name = 'wizard.res.partner.classifier.man'
    _description = 'Wizard para calculo manual de clientes'

    res_partner_id = fields.Many2many('res.partner', string='Clientes')
    date_init = fields.Datetime(string='Fecha de inicio')
    date_end = fields.Datetime(string='Fecha de termino')

    def compute_customers_classifier(self):
        for record in self:
            if len(record.res_partner_id) >= 1:
                for user in record.res_partner_id:
                    if len(user.sale_order_ids):
                        data = user._compute_get_families(self.date_init, self.date_end)
                        print(self.date_init, self.date_end)
                        print(data)
                        rest_id = self.env['awd.res.partner.result'].create({
                                        'partner_id': user.id,
                                        'awd_init_period': self.date_init,
                                        'awd_end_period': self.date_end,
                                        'awd_auto_compute': False,
                                    })
                        data_one = user._get_fam_qty_cost(data, rest_id)
                        data_two = user._get_fam_so_qty_cost(data, rest_id)
                        print('Clasificador calculado', user.name)
            else:
                # users = self.env['res.partner'].search([('category_id.name', '=','Cliente')])
                users = self.env['res.partner'].search([])
                for user in users:
                    if len(user.sale_order_ids):
                        data = user._compute_get_families(self.date_init, self.date_end)
                        print(self.date_init, self.date_end)
                        print(data)
                        rest_id = self.env['awd.res.partner.result'].create({
                                        'partner_id': user.id,
                                        'awd_init_period': self.date_init,
                                        'awd_end_period': self.date_end,
                                        'awd_auto_compute': False,
                                    })
                        data_one = user._get_fam_qty_cost(data, rest_id)
                        data_two = user._get_fam_so_qty_cost(data, rest_id)
                        print('Clasificador calculado', user.name)

        return {'type': 'ir.actions.client', 'tag': 'reload'}