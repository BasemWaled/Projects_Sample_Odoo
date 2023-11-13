# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductTemplateInh(models.Model):
    _inherit = "product.template"

    division_id = fields.Many2one('product.division', string="Division")
    product_type_id = fields.Many2one('product.type', string='Type')
    manufacturer_id = fields.Many2one('product.manufacturer', string='Manufacturer')
    brand_id = fields.Many2one('product.brand', string='Brand')
    model_id = fields.Many2one('product.model', string="Model")
    country_origin_id = fields.Many2one('product.country.origin', string='Country Of Origin')
    production_year = fields.Char(string='Production Year')






