# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime


class medical_appointments_invoice_wizard(models.TransientModel):
    _name = "medical.appointments.invoice.wizard"
    _description = "Medical Appointments Invoice Wizard"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    validity_status = fields.Selection([('draft', 'Draft'), ('invoice', 'Invoice Created'), ('cancel', 'Cancelled')],
                                       string="Validity Status", default='draft', readonly=True)

    def create_invoice(self):
        appointment = self.env["clinic.appointment"].browse(self.env.context.get("active_id"))

        # Create the invoice using the sequence defined in the XML file
        sequence = self.env.ref("clinic_management.clinic_appointments_invoice_sequence")
        invoice_vals = {"move_type": "out_invoice", "partner_id": appointment.patient_id.id,
                        "invoice_date": fields.Date.today(), "invoice_line_ids": [(0, 0, {
                "product_id": appointment.consultations_id.id, "name": appointment.consultations_id.name, "quantity": 1,
                "price_unit": appointment.consultations_id.lst_price,
                "tax_ids": [(6, 0, appointment.consultations_id.taxes_id.ids)], })], "name": sequence.next_by_id(), }
        invoice = self.env["account.move"].create(invoice_vals)

        # Update the validity status of the wizard
        self.write({"validity_status": "invoice"})
        self.message_post(body=_("Invoice created with reference %s") % invoice.name)
