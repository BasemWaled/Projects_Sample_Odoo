from odoo import http
from odoo.http import request, Response


class ApiController(http.Controller):

    @http.route('/api/auth/login', type='json', auth='none', methods=['POST'], csrf=False)
    def authenticate(self, **kwargs):
        db = kwargs.get('db')
        login = kwargs.get('login')
        password = kwargs.get('password')

        if not db or not login or not password:
            return Response("Missing dbname, login, or password", status=400)

        uid = request.session.authenticate(db, login, password)
        if uid:
            user = request.env['res.users'].sudo().browse(uid)
            return {
                'uid': uid,
                'email': user.email,
                'name': user.name,
                'session_id': request.session.sid,
            }
        else:
            return Response("Invalid login or password", status=401)
