from odoo import http
from odoo.http import request


class WhatsAppLoop(http.Controller):
    @http.route('/whatsapp/', auth='public')
    def whatsapp(self, **kw):
        crm_leads = request.env['crm.lead'].search([])
        output = "<h1>CRM Lead</h1><ul>"
        for lead in crm_leads:
            output += '<li>' + str(lead.contact_name) + " ---- " + str(lead.name) + " ----- " + str(
                lead.phone) + '</li>'
        output += "</ul>"
        return output

    @http.route('/get_crm', type='json', auth='public')
    def get_crm(self, **kw):
        crm_leads = request.env['crm.lead'].search([])
        data = []
        for lead in crm_leads:
            vals = {
                'contact_name': lead.contact_name,
                'name': lead.name,
                'phone': lead.phone
            }
            data.append(vals)
        response = {'status': 200, 'response': data, 'message': "Successfully fetched data from CRM"}
        return response

    @http.route('/create_crm1', type='json', auth='public')
    def create_crm(self, **rec):
        if rec.get('contact_name') and rec.get('phone') and rec.get('name'):
            existing_partner = request.env['res.partner'].sudo().search([
                ('name', '=', rec['contact_name']),
                ('phone', '=', rec['phone'])
            ])
            if existing_partner:
                print("Partner with the same name and phone already exists.")
                partner = existing_partner[0]
            else:
                vals2 = {
                    'name': rec['contact_name'],
                    'phone': rec['phone']
                }
                partner = request.env['res.partner'].sudo().create(vals2)

            vals1 = {
                'phone': rec['phone'],
                'name': rec['name'],
                'partner_id': partner.id
            }
            new_crm = request.env['crm.lead'].sudo().create(vals1)
            args = {'success': True, 'message': 'Successfully created a new CRM Lead', 'id': new_crm.id}
            return args
        else:
            args = {'success': False, 'message': 'Contact name, phone, and name are required fields'}
            return args

# ______________________________________________________________________________________________________________________

# class paykmatrix(http.Controller):
#     @http.route('/paykmatrix/', auth='public')
#     def index(self, **kw):
#         sales_orders = http.request.env['account.move'].search([])
#         output = "<h1>Sales Order</h1><ul>"
#         for sale in sales_orders:
#             output += '<li>' + sale['invoice_partner_display_name'] + "  " + sale['name'] + "  " + sale[
#                 'payment_state'] + '</li>'
#         output += "</ul>"
#         return output
#
#     @http.route('/get_patients_km', type='json', auth='user')
#     def get_patients(self):
#         print("yes here entered")
#         patients_rec = request.env['account.move'].search([])
#         patients = []
#         for rec in patients_rec:
#             vals = {
#                 'name': rec.name,
#                 'invoice_partner_display_name': rec.invoice_partner_display_name,
#                 'payment_state': rec.payment_state,
#             }
#             patients.append(vals)
#         print("patient List ---->", patients)
#         data = {'status': 200, 'response': patients, 'message': 'nice success'}
#         return data
#
#     @http.route('/create_patient_1', type='json', auth='user')
#     def create_patient(self, **rec):
#         if request.jsonrequest:
#             print("rec", rec)
#             if rec['partner_id']:
#                 vals = {
#                     'invoice_partner_display_name': rec['invoice_partner_display_name'],
#                     'name': rec['name']
#                 }
#         new_patient = request.env['account.move'].sudo().create(vals)
#         print("New Patient Is ", new_patient)
#         args = {'success': True, 'message': 'Success created new patient', 'id': new_patient.id}
#         return args

# @http.route('/create_patient_basem', type='json', auth='user')
# def create_patient(self, **rec):
#     if request.jsonrequest:
#         print("rec", rec)
#         vals = {}
#         if 'invoice_partner_display_name' in rec:
#             vals['invoice_partner_display_name'] = rec['invoice_partner_display_name']
#
#         new_patient = request.env['account.move'].sudo().create(vals)
#         print("New Patient Is ", new_patient)
#         args = {'success': True, 'message': 'Successfully created a new patient', 'id': new_patient.id}
#     return args
