from pprint import pprint
from datetime import datetime
import base64
import time
import json
# from base64 import b64encode
# from json import dumps
from odoo import http


class InvoiceOdooController(http.Controller):
    @http.route('/web/session/auth', type='json', auth="none", csrf=False, cors="*")
    def authenticate(self, db, login, password, base_location=None):
        http.request.session.authenticate(db, login, password)
        return http.request.env['ir.http'].session_info()

    @http.route('/api/validate_sale', type='json', auth='none', csrf=False, methods=['POST'], cors="*")
    def data_validate(self, **kw):
        try:
            data = http.request.jsonrequest
            # print(data)
            userdata = data['params']['datauser']
            sale = http.request.env['sale.order'].sudo().search([
                                ('name', '=', userdata['num_order']),
                                ('state', 'not in', ['draft', 'cancel', 'to_approve']),
                                ], limit=1)

            if sale.id:
                if userdata['total'] != json.loads(sale.tax_totals_json)['amount_total']:
                    resp = {'error': 'No coincide la cantidad'}
                    return resp

                resp = {
                    'client': {
                        'name': sale.partner_id.name,
                        'rfc': sale.partner_id.vat,
                        'zip': sale.partner_id.zip,
                        'street_name': sale.partner_id.street_name,
                        'street_number': sale.partner_id.street_number,
                        'street_number2': sale.partner_id.street_number2,
                        'colony': sale.partner_id.l10n_mx_edi_colony,
                        'state': sale.partner_id.state_id.name,
                        'country': sale.partner_id.country_id.name
                        },
                    'sale': {
                        'sale_id': sale.id,
                        'sale_team': sale.team_id.name,
                        'date': sale.date_order.strftime("%d/%m/%Y"),
                        'total': json.loads(sale.tax_totals_json)['amount_total']
                        }
                    }
                return resp
            else:
                resp = {'error': 'No exiten datos de venta'}
                return resp

        except Exception as e:
            resp = {'error': e}
            return resp

    @http.route('/api/get_invoice', type='json', auth='user', methods=['POST'], csrf=False, cors="*")
    def invoice_get(self, **kw):
        try:
            resp = {}
            data = http.request.jsonrequest
            data = data['params']
            sale = http.request.env['sale.order'].sudo().search([
                                    ('id', '=', data['invoice']['id'])
                                    ], limit=1)
            if sale.id:
                # GET XML
                if sale.invoice_status == 'to invoice':

                    if sale.partner_id.name == 'PUBLICO EN GENERAL':
                        partner_id = self._create_client(data)
                        sale.partner_id = partner_id
                        sale.partner_invoice_id = partner_id
                        sale.partner_shipping_id = partner_id
                    else:
                        sale.partner_id.vat = data['client']['rfc']
                        sale.partner_id.name = data['client']['name']
                        sale.partner_id.zip = data['client']['postal_code']

                    in_id = self.make_invoice(sale, data, '1', None)
                    resp['invoice_id'] = in_id
                    ## GET XML AND PDF
                    resp['invoice_edo'] = 'Factura creada correctamente'
                    return resp

                elif sale.invoice_status == 'invoiced':
                    invoices = sale.invoice_ids
                    for invoice in invoices:
                        if invoice.state == 'draft':
                            in_id = self.make_invoice(sale, data, '2', invoice)
                            # invoice.action_post()
                            resp['invoice_id'] = in_id
                            ## GET XML AND PDF
                            invoice = http.request.env['account.move'].sudo().search([
                                ('id', '=', in_id),
                                ], limit=1)
                            for edi_doc in invoice.edi_document_ids:
                                if 'CFDI' in edi_doc.edi_format_name:
                                    resp['XML'] = {
                                        # 'xml_raw': edi_doc.attachment_id.raw,
                                        'base64': edi_doc.attachment_id.datas.decode('utf-8'),
                                        }
                                else:
                                    resp['errors'] = {
                                        'xml_error': 'No hay xml CFDI asociado',
                                        }
                        if invoice.state == 'posted':
                            resp['invoice_id'] = invoice.id
                            for edi_doc in invoice.edi_document_ids:
                                if 'CFDI' in edi_doc.edi_format_name:
                                    resp['XML'] = {
                                        # 'xml_raw': edi_doc.attachment_id.raw,
                                        'base64': edi_doc.attachment_id.datas.decode('utf-8'),
                                        }
                                else:
                                    resp['errors'] = {
                                        'xml_error': 'No hay xml CFDI asociado',
                                        }

                # GET PDF
                if "XML" in resp:
                    pdf = http.request.env.ref('account.account_invoices').sudo()._render_qweb_pdf([resp['invoice_id']])
                    b64_pdf = base64.b64encode(pdf[0])
                    resp['pdf'] = {
                        'base64': b64_pdf.decode('utf-8'),
                        }
                    resp['code'] = 201
                    return resp
                else:
                    resp = {'error': 'Error al generar XML'}
                    return resp
            else:
                resp = {'error': 'No hay datos de venta'}
                return resp

        except Exception as e:
            resp = {'error': e}
            return resp
    
    def make_invoice(self, sale, data, step, invoice=None):
        if step == '1':
            sale.picking_ids.partner_id = sale.partner_id
            invoice = sale._create_invoices()

        if data['invoice']['forma_pago']:
            invoice.l10n_mx_edi_payment_method_id.code = data['invoice']['forma_pago']
        else:
            invoice.l10n_mx_edi_payment_method_id.code = '03'
        if data['invoice']['uso']:
            invoice.l10n_mx_edi_usage = data['invoice']['uso']
        else:
            invoice.l10n_mx_edi_usage = 'G03'
        
        # if data['invoice']['fecha_vencimiento']:
            # invoice.invoice_date_due = lambda *a: time.strftime('%Y-%m-%d')

        print(invoice.partner_id.id)
        invoice.action_post()
        return invoice.id

    def _create_client(self, data):
        partner_id = http.request.env['res.partner'].sudo().search([
                                    ('vat', '=', data['client']['rfc'])
                                ], limit=1)

        if partner_id.id:
            partner_id.vat = data['client']['rfc']
            partner_id.name = data['client']['name']
            partner_id.zip = data['client']['postal_code']
            print('## No Create', partner_id.id)
            return partner_id.id

        values = {
            'name': data['client']['name'],
            'vat': data['client']['rfc'],
            'zip': data['client']["postal_code"]
        }

        partner = http.request.env['res.partner'].sudo().create(values)
        return partner.id