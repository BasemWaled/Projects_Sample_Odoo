# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ProducttemplateInh(models.Model):
    _inherit = "product.template"

    division = fields.Char(string='Division')
    product_type = fields.Char(string='Type')
    manufacturer = fields.Char(string='Manufacturer')
    brand = fields.Char(string='Brand')
    model = fields.Char(string='Model')
    country_of_origin = fields.Char(string='Country Of Origin')
    production_year = fields.Char(string='Production Year')






