# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductModel(models.Model):
    _name = 'product.model'
    _rec_name = 'name'
    name = fields.Char()


class ProductDivision(models.Model):
    _name = 'product.division'
    _rec_name = 'name'
    name = fields.Char()


class ProductType(models.Model):
    _name = 'product.type'
    _rec_name = 'name'
    name = fields.Char()


class ProductManufacturer(models.Model):
    _name = 'product.manufacturer'
    _rec_name = 'name'
    name = fields.Char()


class ProductBrand(models.Model):
    _name = 'product.brand'
    _rec_name = 'name'
    name = fields.Char()


class ProductCountryOrigin(models.Model):
    _name = 'product.country.origin'
    _rec_name = 'name'
    name = fields.Char()
