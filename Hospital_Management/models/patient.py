from odoo import api, fields, models


class Hospitalpatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital patient"

    Name = fields.Char(string='Name')
    Mobile = fields.Char(string='Mobile')
    Age = fields.Integer(string='Age')
    Gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    Description = fields.Text(string='Description')
    active = fields.Boolean(string='active', default=True)