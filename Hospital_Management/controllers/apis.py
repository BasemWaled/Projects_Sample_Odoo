from odoo import http


class ApiController(http.Controller):
    @http.route('/Hospital_Management/Hospital_Management/', auth='public')
    def index(self, **kw):
        sales_orders = http.request.env['sale.order'].search([])
        output = "<h1> Sales Order</h1><ul>"

        for sale in sales_orders:
            output += '<li>' + sale['name'] + '</li>'
        return output
