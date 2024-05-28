import json
import math
import logging
import requests
from odoo import http, _, exceptions
from odoo.http import request

_logger = logging.getLogger(__name__)


class OdooAPI(http.Controller):
    @http.route('/auth/', type='json', auth='none', methods=["POST"], csrf=False)
    def authenticate(self, *args, **post):
        try:
            login = post.get("login")
            password = post.get("password")
            db = post.get("db")
        except KeyError as e:
            error_msg = f"`{e.args[0]}` is required."
            _logger.error(error_msg)
            return self.error_response(exceptions.AccessDenied(), error_msg)

        try:
            request.session.authenticate(db, login, password)
            res = self.session_info()
            return res
        except exceptions.AccessDenied as e:
            _logger.error(str(e))
            return self.error_response(e, str(e))
        except Exception as e:
            _logger.exception("An error occurred during authentication.")
            return self.error_response(e, "An error occurred during authentication.")

    @staticmethod
    def error_response(error, msg):
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": 200,
                "message": msg,
                "data": {
                    "name": str(error),
                    "debug": "",
                    "message": msg,
                    "arguments": list(error.args),
                    "exception_type": type(error).__name__
                }
            }
        }

    @staticmethod
    def session_info():
        return {
            "jsonrpc": "2.0",
            "id": None,
            "result": {
                "session_id": request.session.sid,
                "uid": request.session.uid,
                "username": request.env.user.name,
                "db": request.env.cr.dbname,
            }
        }

    @http.route('/get/pro', type='json', auth='user', methods=["GET"], csrf=False)
    def get_products(self, **kwargs):
        try:
            Product = request.env['product.product']
            products = Product.search([])
            product_list = []
            for product in products:
                product_info = {
                    "id": product.id,
                    "name": product.name,
                    "internal_reference": product.default_code,
                    "sales_price": product.lst_price,
                }
                product_list.append(product_info)
            return {
                "jsonrpc": "2.0",
                "id": None,
                "result": product_list
            }
        except Exception as e:
            _logger.exception("An error occurred while fetching products.")
            return self.error_response(e, "An error occurred while fetching products.")
