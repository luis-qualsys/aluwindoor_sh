import datetime
from dataclasses import field
from odoo import models, fields, api

class AwdResPartnerResults(models.Model):
    _name = 'awd.res.partner.result'
    _description = 'Resultados de calculo'

    partner_id =  fields.Many2one('res.partner', string='Parner ID')
    awd_init_period = fields.Date(string='Periodo de inicio')
    awd_end_period = fields.Date(string='Periodo de termino')
    awd_category = fields.Selection(string='Categoria', selection=[
                                        ('0', 'Ninguno'),
                                        ('1', 'Bronce'),
                                        ('2', 'Planta'),
                                        ('3', 'Oro'),
                                    ], default="0", compute='_get_category_client')
    awd_auto_compute = fields.Boolean(string='Es automatico', default=False)
    awd_family_counter = fields.Integer(string='Numero de familias', compute='_get_families_number', store=True, help="Numero de familias de productos compradas durante el periodo")
    awd_freq_sales = fields.Float(string='Frecuencia de venta', compute='_get_frequencies_sales', help="Frecuencia de ventas durante el periodo")
    awd_aver_sales = fields.Float(string='Promedio de venta', compute='_get_average_sales', help="Promedio de ventas durante el periodo")
    awd_sold_sales = fields.Float(string='Venta de periodo', compute='_get_sold_sales', help="Cantidad de ventas durante el periodo")

    awd_calculate_results_id = fields.One2many(comodel_name='awd.res.partner.computed', inverse_name='awd_parner_result_id', string='Calculo de categorias')
    awd_calculate_so_results_id = fields.One2many(comodel_name='awd.res.partner.computed.so', inverse_name='awd_parner_result_id', string='Calculo de ventas')

    @api.depends('awd_calculate_results_id')
    def _get_sold_sales(self):
        for record in self:
            sold = 0.0
            for family in record.awd_calculate_results_id:
                sold += family.awd_family_sales
            record.awd_sold_sales = sold

    @api.depends('partner_id')
    def _get_frequencies_sales(self):
        for record in self:
            date = record.awd_end_period - record.awd_init_period
            date_init = datetime.datetime.combine(record.awd_init_period, datetime.time(0, 0))
            date_end = datetime.datetime.combine(record.awd_end_period, datetime.time(0, 0)) + datetime.timedelta(days=1, microseconds=-1)
            orders = self.env['sale.order'].search([
                                ('partner_id', '=', record.partner_id.id), 
                                ('date_order', '>=', date_init),
                                ('date_order', '<=', date_end),
                                ('state', '=', 'sale')
                                ])
            if len(orders) > 0:
                dates = []
                for sale in orders:
                    dates.append(sale.date_order.date())
                sales = len(set(dates))
                record.awd_freq_sales = sales / (date.days + 1)
            else:
                record.awd_freq_sales = 0.0

    @api.depends('awd_calculate_so_results_id')
    def _get_average_sales(self):
        for record in self:
            if len(record.awd_calculate_so_results_id) > 0:
                spantime = record.awd_end_period - record.awd_init_period
                record.awd_aver_sales = len(record.awd_calculate_so_results_id) / (spantime.days + 1)
            else:
                record.awd_aver_sales = 0.0


    @api.depends('awd_calculate_results_id')
    def _get_families_number(self):
        for record in self:
            counter = 0
            for family in record.awd_calculate_results_id:
                counter += 1
            record.awd_family_counter = counter

    @api.depends('awd_calculate_results_id', 'awd_calculate_so_results_id')
    def _get_category_client(self):
        for record in self:
            datas = record._compute_stats()
            # print("######### DATAS", datas)
            if datas == 1:
                record.awd_category = '1'
            if datas == 2:
                record.awd_category = '2'
            if datas == 3:
                record.awd_category = '3'
            if datas == 0:
                record.awd_category = '0'


    def _compute_stats(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        awd_families = int(ICPSudo.get_param('awd_customer_classifier.awd_families_stat'))
        awd_sales = int(ICPSudo.get_param('awd_customer_classifier.awd_sale_stat_min'))
        awd_freq = int(ICPSudo.get_param('awd_customer_classifier.awd_freq_sales'))
        for record in self:
            # print(record.awd_init_period, record.awd_end_period)
            n_fam = len(record.awd_calculate_results_id)
            # families = self.env['awd.product.family'].search_count([('awd_active_compute', '=', True), ('company_id', '=', self.env.company.id)])
            # print("####Familias",n_fam)
            # Numero de familias vendidas
            fams_fin = False
            if n_fam >= awd_families:
                fams_fin = True
            
            # print("#### Fam_fin", fams_fin)
            # Frecuencia de ventas
            freq_fin = record.awd_freq_sales * 100
            freq = False
            if freq_fin >= awd_freq:
                freq = True

            # print("#### Freq", freq)
            # Cantidad vendida
            prices = False
            if record.awd_sold_sales >= awd_sales:
                prices = True

            # print('## Prices', prices)
            datas = [fams_fin, freq, prices]

            return datas.count(True)

    def make_dictionary_templates(self, dictionary_empty, key):
        if key in dictionary_empty:
            dictionary_empty[key] += 1
        else:
            dictionary_empty[key] = 1

class AwdResPartnerCompute(models.Model):
    _name = 'awd.res.partner.computed'
    _description = 'Calculo de ventas por familia'

    awd_parner_result_id = fields.Many2one('awd.res.partner.result', string='Resultado')
    awd_familia = fields.Char(string='Familia')
    awd_family_sales = fields.Float(string='Cantidad Monetaria')
    awd_family_qty = fields.Integer(string='Cantidad de Productos')

class AwdResPartnerComputeSO(models.Model):
    _name = 'awd.res.partner.computed.so'
    _description = 'Calculo de ventas por ordenes'

    awd_parner_result_id = fields.Many2one('awd.res.partner.result', string='Resultado')
    awd_sale_order = fields.Char(string='Orden de venta')
    awd_family = fields.Char(string='Familia')
    awd_family_qty = fields.Integer(string='Cantidad')

