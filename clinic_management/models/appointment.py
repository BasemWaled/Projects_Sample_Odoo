from odoo import api, fields, models, _
# from datetime import datetime, date
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class clinic_appointment(models.Model):
    _name = 'clinic.appointment'
    _description = 'Medical Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Appointment ID", readonly=True, copy=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('clinic.appointment'))
    patient_id = fields.Many2one('clinic.patient', string="Patient", required=True)
    doctor_id = fields.Many2one('res.partner', 'Doctor', required=True)
    appointment_date = fields.Datetime('Appointment Date', required=True, default=fields.Datetime.now)
    appointment_end = fields.Datetime('Appointment End', required=True)
    patient_status = fields.Selection(
        [('ambulatory', 'Ambulatory'), ('outpatient', 'Outpatient'), ('inpatient', 'Inpatient'), ], 'Patient status',
        sort=False, default='outpatient')
    validity_status = fields.Selection([('invoice', 'Invoice'), ('tobe', 'To be Invoiced'), ], 'Status', sort=False,
                                       readonly=True, default='tobe')
    comments = fields.Text(string="Info")
    duration = fields.Integer('Duration')
    urgency_level = fields.Selection([('a', 'Normal'), ('b', 'Urgent'), ('c', 'Medical Emergency'), ], 'Urgency Level',
                                     sort=False, default="b")
    consultations_id = fields.Many2one('product.product', 'Consultation Service', required=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('in_consultation', 'In Consultation'), ('done', 'Done'), ('cancel', 'Cancelled')],
        default='draft', string="Status", required=True, tracking=True)

    def action_in_consultation(self):
        self.state = 'in_consultation'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'
