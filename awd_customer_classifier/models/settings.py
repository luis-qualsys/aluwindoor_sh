from odoo import models, fields, api

class ParnerClassifierSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    awd_partner_freq_compute = fields.Integer(string='Frecuencia de cálculo de clasificador (días)')
    awd_partner_freq_date_init = fields.Date(string='Fecha de inicio del cálculo')
    awd_families_stat = fields.Integer(string="Cantidad de familias")
    awd_sale_stat_min = fields.Integer(string="Cantidad minima para clasificador")
    awd_freq_sales = fields.Integer(string="Frecuencia de venta")

    def set_values(self):
        res = super(ParnerClassifierSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('awd_customer_classifier.awd_partner_freq_compute', self.awd_partner_freq_compute)
        self.env['ir.config_parameter'].set_param('awd_customer_classifier.awd_partner_freq_date_init', self.awd_partner_freq_date_init)
        self.env['ir.config_parameter'].set_param('awd_customer_classifier.awd_families_stat', self.awd_families_stat)
        self.env['ir.config_parameter'].set_param('awd_customer_classifier.awd_sale_stat_min', self.awd_sale_stat_min)
        self.env['ir.config_parameter'].set_param('awd_customer_classifier.awd_freq_sales', self.awd_freq_sales)
        return res

    @api.model
    def get_values(self):
        res = super(ParnerClassifierSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        awd_partner_freq_compute = ICPSudo.get_param('awd_customer_classifier.awd_partner_freq_compute')
        awd_partner_freq_date_init = ICPSudo.get_param('awd_customer_classifier.awd_partner_freq_date_init')
        awd_families_stat = ICPSudo.get_param('awd_customer_classifier.awd_families_stat')
        awd_sale_stat_min = ICPSudo.get_param('awd_customer_classifier.awd_sale_stat_min')
        awd_freq_sales = ICPSudo.get_param('awd_customer_classifier.awd_freq_sales')
        res.update(
            awd_partner_freq_compute = awd_partner_freq_compute,
            awd_partner_freq_date_init = awd_partner_freq_date_init,
            awd_families_stat = awd_families_stat,
            awd_sale_stat_min = awd_sale_stat_min ,
            awd_freq_sales = awd_freq_sales
        )

        return res