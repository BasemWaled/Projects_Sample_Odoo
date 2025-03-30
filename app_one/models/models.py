from odoo import models, fields

class PropertyModel(models.Model):
    _name = "property.model"
    _description = "Property Model"

    name = fields.Char(string="Name")
    postcode = fields.Char(string="Postcode")
    date_available = fields.Date(string="Date Available")
