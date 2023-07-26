# -*- coding: utf-8 -*-
# from odoo import http


# class OdooLearn(http.Controller):
#     @http.route('/odoo_learn/odoo_learn', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_learn/odoo_learn/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_learn.listing', {
#             'root': '/odoo_learn/odoo_learn',
#             'objects': http.request.env['odoo_learn.odoo_learn'].search([]),
#         })

#     @http.route('/odoo_learn/odoo_learn/objects/<model("odoo_learn.odoo_learn"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_learn.object', {
#             'object': obj
#         })
