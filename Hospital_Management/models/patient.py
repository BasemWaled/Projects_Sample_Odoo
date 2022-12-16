from odoo import api, fields, models


class Hospitalpatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital patient"

    name = fields.Char(string='Name', tracking=True)
    mobile = fields.Char(string='Mobile', tracking=True)
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True, default='female')
    description = fields.Text(string='Description', tracking=True)
    active = fields.Boolean(string='active', default=True)
