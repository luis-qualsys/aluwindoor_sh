from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    awd_payment_methods = fields.Many2one('l10n_mx_edi.payment.method', string='Metodo de pago')
    awd_usage_invoice = fields.Selection(
        selection=[
            ('G01', 'Adquisición de mercania'),
            ('G02', 'Returns, discounts or bonuses'),
            ('G03', 'Gastos en General'),
            ('I01', 'Construcciones'),
            ('I02', 'Mobiliario y equipo de oficina por inversiones'),
            ('I03', 'Equipo de transporte'),
            ('I04', 'Equipo de computo y accesorios'),
            ('I05', 'Dados, troqueles, moldes, matrices y herramental'),
            ('I06', 'Comunicaciones telefónicas'),
            ('I07', 'Comunicaciones satelitales'),
            ('I08', 'Otra maquinaria y equipo'),
            ('D01', 'Honorarios médicos, dentales y gastos hospitalarios'),
            ('D02', 'Gastos medicos por incapacidad o discapacidad'),
            ('D03', 'Gastos funerarios'),
            ('D04', 'Donativos'),
            ('D05', 'Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación)'),
            ('D06', 'Apartaciones voluntarias al SAR'),
            ('D07', 'Primas por seguros de gastos médicos'),
            ('D08', 'Gastos por transportación escolar obligatoria'),
            ('D09', 'Depositos en cuentas para el ahorro, primas que tengan como base planes de pensiones'),
            ('D10', 'Pagos por servicios educativos (colegiaturas)'),
        ],
        string="Uso de CFDI", default='G03')