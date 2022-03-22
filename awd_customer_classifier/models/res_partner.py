import datetime

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    awd_calculate_results = fields.One2many(comodel_name='awd.res.partner.result', inverse_name='partner_id', string='Resultados de calculo')
    awd_category = fields.Selection(string='Categoria', selection=[
                                        ('0', 'Ninguno'),
                                        ('1', 'Bronce'),
                                        ('2', 'Plata'),
                                        ('3', 'Oro')
                                    ], default="0", compute='_get_categories')

    @api.depends('awd_calculate_results')
    def _get_categories(self):
        for record in self:
            result = self.env['awd.res.partner.result'].search([('partner_id.id', '=', record.id)])
            if len(result) > 0:
                result = result[-1]
                if result.awd_category:
                    record.awd_category = result.awd_category
                else:
                    record.awd_category = '0'
            else:
                record.awd_category = '0'

    def compute_customer_classifier(self):
        users = self.env['res.partner'].search([])
        for user in users:
            # checker, date_init, date_end = user._get_dates_init()
            ICPSudo = self.env['ir.config_parameter'].sudo()
            period = int(ICPSudo.get_param('awd_customer_classifier.awd_partner_freq_compute'))
            date_init, date_end = user._get_dates_init(period)
            # print(date_init, date_end)
            if len(user.awd_calculate_results) >= period + 1:
                results = sorted(user.awd_calculate_results)[::-1]
                results_not_unlinked = results[:period]
                for result in results:
                    if result not in results_not_unlinked:
                        result.unlink()
                if len(user.sale_order_ids):
                    data = user._compute_get_families(date_init, date_end)
                    rest_id = self.env['awd.res.partner.result'].create({
                            'partner_id': user.id,
                            'awd_init_period': date_init,
                            'awd_end_period': date_end,
                            'awd_auto_compute': True,
                        })
                    data_one = user._get_fam_qty_cost(data, rest_id)
                    data_two = user._get_fam_so_qty_cost(data, rest_id)
                    print('Clasificador calculado', user.name)
                else:
                    data = user._compute_get_families(date_init, date_end)
                    rest_id = self.env['awd.res.partner.result'].create({
                            'partner_id': user.id,
                            'awd_init_period': date_init,
                            'awd_end_period': date_end,
                            'awd_auto_compute': True,
                        })
                    data_one = user._get_fam_qty_cost(data, rest_id)
                    data_two = user._get_fam_so_qty_cost(data, rest_id)
                    print('Clasificador calculado', user.name)
            else:
                if len(user.sale_order_ids):
                    data = user._compute_get_families(date_init, date_end)
                    rest_id = self.env['awd.res.partner.result'].create({
                            'partner_id': user.id,
                            'awd_init_period': date_init,
                            'awd_end_period': date_end,
                            'awd_auto_compute': True,
                        })
                    data_one = user._get_fam_qty_cost(data, rest_id)
                    data_two = user._get_fam_so_qty_cost(data, rest_id)
                    print('Clasificador calculado', user.name)
                else:
                    data = user._compute_get_families(date_init, date_end)
                    rest_id = self.env['awd.res.partner.result'].create({
                            'partner_id': user.id,
                            'awd_init_period': date_init,
                            'awd_end_period': date_end,
                            'awd_auto_compute': True,
                        })
                    data_one = user._get_fam_qty_cost(data, rest_id)
                    data_two = user._get_fam_so_qty_cost(data, rest_id)
                    print('Clasificador calculado', user.name)
        return True


    def _get_fam_so_qty_cost(self, data, result):
        for user in self:
            records = []
            # print(data)
            for sale in data:
                for fam in sale['families_qty'].keys():
                    record = {
                        'awd_parner_result_id': result.id,
                        'awd_sale_order': sale['name'],
                        'awd_family': fam,
                        'awd_family_qty': sale['families_qty'][fam]
                    }
                    self.env['awd.res.partner.computed.so'].create(record)
                    records.append(record)
        # print(records)
        return records


    def _get_fam_qty_cost(self, data, result):
        for user in self:
            records = []
            dict_cost_efim = {}
            dict_qty_efim = {}
            for sale in data:
                costos = sale['families_cost']
                qty = sale['families_qty']

                for fam in costos.keys():
                    user.make_dictionary_templates(dict_cost_efim, fam, costos[fam])
                    user.make_dictionary_templates(dict_qty_efim, fam, qty[fam])

            for key in dict_qty_efim.keys():
                record = {
                    'awd_parner_result_id': result.id,
                    'awd_familia': key,
                    'awd_family_sales': dict_cost_efim[key],
                    'awd_family_qty': dict_qty_efim[key]
                }
                self.env['awd.res.partner.computed'].create(record)
                records.append(record)
        
        return records

    def _compute_get_families(self, date_init, date_end):
        data = []
        for record in self:
            for sale in record.sale_order_ids:
                sales_dat = {}
                if sale.date_order <= date_end and sale.date_order >= date_init:
                    sales_dat['name'] = sale.name
                    fam_names_cost = {}
                    fam_names_qty = {}
                    for order_line in sale.order_line:
                        if  order_line.product_template_id.awd_product_family_id.parent_id.id != False:
                            fam_name = order_line.product_template_id.awd_product_family_id.parent_id.name
                        else:
                            fam_name = order_line.product_template_id.awd_product_family_id.name

                        if order_line.product_template_id.awd_product_family_id != None:
                            self.make_dictionary_templates(fam_names_cost, fam_name, order_line.price_subtotal)
                            self.make_dictionary_templates(fam_names_qty, fam_name, order_line.product_uom_qty)
                        else:
                            self.make_dictionary_templates(fam_names_cost, 'Sin familia', order_line.price_subtotal)
                            self.make_dictionary_templates(fam_names_qty, 'Sin familia', order_line.product_uom_qty)
                    sales_dat['families_cost'] = fam_names_cost
                    sales_dat['families_qty'] = fam_names_qty
                    data.append(sales_dat)
        return data

    def _get_dates_init(self, period):
        # period = int(ICPSudo.get_param('awd_customer_classifier.awd_partner_freq_compute'))
        # date_init = ICPSudo.get_param('awd_customer_classifier.awd_partner_freq_date_init')
        today = datetime.datetime.today()
        date_end = today - datetime.timedelta(days=period)

        # print(date_init, today)
        return today, date_end
        # date_init_aut = None

        # dates = []
        # for results in self.awd_calculate_results:
        #     if results.awd_auto_compute:
        #         dates.append(results.awd_end_period)

        # if dates:
        #     date_init_aut = sorted(dates)[-1]

        # if date_init_aut:
        #     date_init = date_init_aut

        # date_end = date_init + datetime.timedelta(days=period)

        # date_init = datetime.datetime.combine(date_init, datetime.time(0, 0))
        # date_end = datetime.datetime.combine(date_end, datetime.time(0, 0)) + datetime.timedelta(days=1, microseconds=-1)
        # # today = datetime.datetime.today()

        # if date_init == ICPSudo.get_param('awd_customer_classifier.awd_partner_freq_date_init'):
        #     return True, date_init, date_end
        # else:
        #     if today >= date_init and today < date_end:
        #         return True, date_init, date_end
        #     if today <= date_init:
        #         return False, date_init, date_end
        #     else:
        #         return True, date_init, date_end

    def make_dictionary_templates(self, dictionary_empty, key, value):
        if key in dictionary_empty:
            dictionary_empty[key] += value
        else:
            dictionary_empty[key] = value