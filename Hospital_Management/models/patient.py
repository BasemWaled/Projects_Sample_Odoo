from odoo import api, fields, models
from datetime import date


class Hospitalpatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital patient"

    name = fields.Char(string='Name', tracking=True)
    date_of_birth = fields.Date(string='Date of Birth')
    mobile = fields.Char(string='Mobile', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True, default='female')
    description = fields.Text(string='Description', tracking=True)
    active = fields.Boolean(string='active', default=True)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 1