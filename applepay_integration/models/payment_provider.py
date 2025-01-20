from odoo import api, fields, models


class PaymentProviderApplePay(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(selection_add=[('applepay', 'Apple Pay')], ondelete={'applepay': 'set default'})
    applepay_entity_id = fields.Char(string='Entity ID', required_if_code='applepay')
    applepay_authorization_bearer = fields.Char(string='Authorization Token', required_if_code='applepay')

    def _get_authorize_urls(self):
        base_url = self.get_base_url()
        """ ApplePay URLS """
        return base_url + '/payment/applepay/render'

