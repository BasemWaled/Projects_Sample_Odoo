from odoo import http
from odoo.http import request


class DashboardManager(http.Controller):

    @http.route('/dashboard/company', type='json', auth='user', methods=['GET'])
    def get_user_company(self):
        user = request.env.user
        company = user.company_id
        return {
            'company_id': company.id,
            'company_name': company.name
        }

# from odoo import http
# from odoo.http import request
#
#
# class DashboardManager(http.Controller):
#
#     @http.route('/dashboard/bills/count', type='json', auth='public', methods=['GET'])
#     def get_bill_count(self):
#         bill_count = request.env['account.move'].search_count([('move_type', '=', 'in_invoice')])
#         return {'bill_count': bill_count}
