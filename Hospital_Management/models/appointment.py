import random
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'patient_id'
    # _rec_name = 'name'
    _order = 'id desc'

    name = fields.Char(string='Sequence', default='new', readonly=True)
    # patient_id = fields.Many2one('hospital.patient', string='patient', ondelete='restrict')
    patient_id = fields.Many2one('hospital.patient', string='patient', ondelete='cascade')
    gender = fields.Selection(related='patient_id.gender', readonly=False)
    ref = fields.Char(related='patient_id.ref', string='reference')
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    description = fields.Text(string='Description', help="Description of the patient from patient record")
    prescription = fields.Html(string='prescription')
    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], string="Priority")
    state = fields.Selection(
        [('draft', 'Draft'), ('in_consultation', 'In Consultation'), ('done', 'Done'), ('cancel', 'Cancelled')],
        default='draft', string="Status", required=True, tracking=True)
    doctor_id = fields.Many2one('res.users', string='Doctor', tracking=True)
    appointment_pharmacy_ines = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')
    hide_sales_price = fields.Boolean(string="Hide Sales Price")
    operation_id = fields.Many2one('hospital.operation', string='Operation', tracking=True)
    progress = fields.Integer('Progress', compute='_compute_progress')
    duration = fields.Float("Duration")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super(HospitalAppointment, self).create(vals)

    def write(self, vals):
        if not self.name and not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super(HospitalAppointment, self).write(vals)

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.description = self.patient_id.description

    def action_test(self):
        print("hallo")
        return {'effect': {'fadeout': 'slow', 'message': 'Click Successfully', 'type': 'rainbow_man', }}

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        action = self.env.ref('Hospital_Management.action_cancel_appointment').read()[0]
        return action

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError(_("you can't delete because this appointment is done"))
        return super(HospitalAppointment, self).unlink()

    # @api.depends('state')
    # def _compute_progress(self):
    #     for rec in self:
    #         if rec.state == 'draft':
    #             progress = 25
    #         elif rec.state == 'in_consultation':
    #             progress = 50
    #         elif rec.state == 'done':
    #             progress = 100
    #         else:
    #             progress = 0
    #         rec.progress = progress
    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = random.randrange(0, 25)
            elif rec.state == 'in_consultation':
                progress = random.randrange(25, 99)
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(string='Price', related='product_id.list_price')
    qty = fields.Integer(string='Quantity', default=1)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
