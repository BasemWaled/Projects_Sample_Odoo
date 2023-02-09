from odoo import fields, models


class ModelName(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='color')
    color_2 = fields.Char(string='color 2')
