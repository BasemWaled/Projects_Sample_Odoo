import logging

from werkzeug import urls
import re
from odoo import _, api, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare

from odoo.addons.payment_applepay.controllers.main import ApplepayController

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'applepay':
            return res

        base_url = self.provider_id.get_base_url()
        rendering_values = self.provider_id.applepay_form_generate_values(processing_values)
        rendering_values.update({
            'api_url': self.provider_id._get_authorize_urls(),
        })
        return rendering_values
