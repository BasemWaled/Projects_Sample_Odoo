from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError
from datetime import datetime
import requests
import json
import logging

_logger = logging.getLogger(__name__)


class ApplePayController(http.Controller):

    @http.route('/payment/applepay/render', type='http', auth='public', website=True)
    def render_applepay_template(self):
        # Search for the Apple Pay payment provider
        applepay_provider = request.env['payment.provider'].sudo().search([('code', '=', 'applepay')], limit=1)
        if not applepay_provider:
            raise UserError(_("Apple Pay provider not configured."))

        # Check the state of the payment provider
        if applepay_provider.state == 'test':
            # Render the test template
            return request.render('payment_applepay_integration.payment_applepay_card_test', {
                'return_url': '/payment/return',
                'check_out_id': 'test_checkout_id',  # Replace with the actual test checkout ID if required
            })
        else:
            # Render the live template
            return request.render('payment_applepay_integration.payment_applepay_card_live', {
                'return_url': '/payment/return',
                'check_out_id': 'live_checkout_id',  # Replace with the actual live checkout ID if required
            })

    @http.route(['/payment/applepay/checkout'], type='http', auth='public', methods=['POST'], csrf=False)
    def applepay_checkout_and_invoice(self, **kwargs):
        try:
            # Log received data for debugging
            _logger.info(f"Received data: {kwargs}")

            # Ensure the user is not a public user
            user = request.env.user
            if user._is_public():
                raise UserError(_("Access Denied: You must be a portal or internal user to complete this transaction."))

            # Extract payment data from request
            amount = kwargs.get('amount')
            currency = kwargs.get('currency', 'SAR')  # Default to SAR if not provided
            payment_type = kwargs.get('paymentType', 'DB')  # Default to DB if not provided
            payment_brand = kwargs.get('paymentBrand', 'APPLEPAY')  # Default to APPLEPAY if not provided

            # Validate required fields
            if not all([amount, payment_type, payment_brand]):
                raise UserError(_('Missing required payment data'))

            # Get the Payment Provider configuration for Apple Pay
            provider = request.env['payment.provider'].sudo().search([('code', '=', 'applepay')], limit=1)
            if not provider:
                raise UserError(_("Apple Pay provider configuration not found."))

            entity_id = provider.applepay_entity_id
            authorization_bearer = provider.applepay_authorization_bearer
            headers = {
                'Authorization': f'Bearer {authorization_bearer}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            # Prepare payload for the payment gateway
            payload = {
                "entityId": entity_id,
                "amount": amount,
                "currency": currency,
                "paymentType": payment_type,
                "paymentBrand": payment_brand,
                "card.number": kwargs.get('card.number'),
                "card.expiryMonth": kwargs.get('card.expiryMonth'),
                "card.expiryYear": kwargs.get('card.expiryYear'),
                "threeDSecure.verificationId": kwargs.get('threeDSecure.verificationId'),
                "threeDSecure.eci": kwargs.get('threeDSecure.eci'),
                "applePay.source": kwargs.get('applePay.source'),
            }

            # Make the API request using the requests library
            response = requests.post(
                url="https://eu-test.oppwa.com/v1/payments",
                headers=headers,
                data=payload
            )
            response_data = response.json()

            # Process payment response
            if response.status_code == 200 and response_data.get('result', {}).get('code') == '000.100.110':
                # Payment successful: Create an invoice
                invoice_vals = {
                    'move_type': 'out_invoice',
                    'partner_id': user.partner_id.id,
                    'currency_id': request.env['res.currency'].sudo().search([('name', '=', currency)], limit=1).id,
                    'invoice_date': datetime.today().date(),
                    'invoice_line_ids': [(0, 0, {
                        'name': 'Apple Pay Payment',
                        'quantity': 1,
                        'price_unit': float(amount),
                        'account_id': request.env['account.account'].sudo().search(
                            [('account_type', '=', 'income'), ('company_id', '=', user.company_id.id)], limit=1).id
                    })],
                }
                invoice = request.env['account.move'].sudo().create(invoice_vals)
                invoice.action_post()

                return request.make_response(
                    json.dumps({
                        'status': 'success',
                        'message': 'Payment and invoice creation successful',
                        'invoice_id': invoice.id
                    }),
                    headers={'Content-Type': 'application/json'}
                )
            else:
                # Payment failed
                return request.make_response(
                    json.dumps({
                        'status': 'failure',
                        'message': 'Payment failed',
                        'error': response_data.get('result', {}).get('description', 'Unknown error')
                    }),
                    headers={'Content-Type': 'application/json'}
                )

        except UserError as e:
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}),
                headers={'Content-Type': 'application/json'}
            )
        except Exception as e:
            return request.make_response(
                json.dumps(
                    {'status': 'error', 'message': 'An error occurred while processing the request', 'error': str(e)}),
                headers={'Content-Type': 'application/json'}
            )

# from odoo import http, _
# from odoo.http import request
# from odoo.exceptions import UserError
# from datetime import datetime
# import json
#
#
# class ApplePayController(http.Controller):
#
#     @http.route(['/payment/applepay/ecommerce'], type='http', auth='public', methods=['POST'], csrf=False)
#     def applepay_ecommerce_checkout(self, **kwargs):
#         try:
#             # Ensure the user is not a public user
#             user = request.env.user
#             if user._is_public():
#                 raise UserError(_("Access Denied: You must be a portal or internal user to complete this transaction."))
#
#             # Extract payment data from request
#             transaction_reference = kwargs.get('transaction_reference')
#             amount = kwargs.get('amount')
#             currency = kwargs.get('currency', 'SAR')
#             payment_type = kwargs.get('paymentType', 'DB')
#             payment_brand = kwargs.get('paymentBrand', 'APPLEPAY')
#
#             # Validate required fields
#             if not all([transaction_reference, amount, payment_type, payment_brand]):
#                 raise UserError(_('Missing required payment data'))
#
#             # Fetch the payment transaction
#             transaction = request.env['payment.transaction'].sudo().search([('reference', '=', transaction_reference)], limit=1)
#             if not transaction:
#                 raise UserError(_("Transaction not found: %s") % transaction_reference)
#
#             # Call the payment gateway
#             provider = transaction.provider_id
#             entity_id = provider.applepay_entity_id
#             authorization_bearer = provider.applepay_authorization_bearer
#             headers = {
#                 'Authorization': f'Bearer {authorization_bearer}',
#                 'Content-Type': 'application/x-www-form-urlencoded'
#             }
#             payload = {
#                 "entityId": entity_id,
#                 "amount": amount,
#                 "currency": currency,
#                 "paymentType": payment_type,
#                 "paymentBrand": payment_brand,
#             }
#             response = request.post(
#                 url="https://eu-test.oppwa.com/v1/payments",
#                 headers=headers,
#                 data=payload  # Send payload directly as form-urlencoded
#             )
#             response_data = response.json()
#
#             # Update transaction status based on payment response
#             if response.status_code == 200 and response_data.get('result', {}).get('code') == '000.100.110':
#                 transaction.sudo().write({'state': 'done'})
#                 return request.make_response(
#                     json.dumps({'status': 'success', 'message': 'Payment successful', 'transaction_id': transaction.id}),
#                     headers={'Content-Type': 'application/json'}
#                 )
#             else:
#                 transaction.sudo().write({'state': 'error', 'state_message': response_data.get('result', {}).get('description')})
#                 return request.make_response(
#                     json.dumps({'status': 'failure', 'message': 'Payment failed', 'transaction_id': transaction.id}),
#                     headers={'Content-Type': 'application/json'}
#                 )
#
#         except UserError as e:
#             return request.make_response(
#                 json.dumps({'status': 'error', 'message': str(e)}),
#                 headers={'Content-Type': 'application/json'}
#             )
#         except Exception as e:
#             return request.make_response(
#                 json.dumps({'status': 'error', 'message': 'An error occurred while processing the payment', 'error': str(e)}),
#                 headers={'Content-Type': 'application/json'}
#             )
#
#
#     @http.route(['/payment/applepay/checkout'], type='http', auth='public', methods=['POST'], csrf=False)
#     def applepay_checkout(self, **kwargs):
#         # Extract data from form-urlencoded payload
#         token = kwargs.get('token')
#         amount = kwargs.get('amount')
#         currency = kwargs.get('currency', 'SAR')
#         payment_type = kwargs.get('paymentType', 'DB')
#         payment_brand = kwargs.get('paymentBrand', 'APPLEPAY')
#         card_number = kwargs.get('card.number')
#         card_expiry_month = kwargs.get('card.expiryMonth')
#         card_expiry_year = kwargs.get('card.expiryYear')
#         three_ds_verification_id = kwargs.get('threeDSecure.verificationId')
#         three_ds_eci = kwargs.get('threeDSecure.eci')
#         applepay_source = kwargs.get('applePay.source')
#
#         # Get the Payment Provider configuration for Apple Pay
#         provider = request.env['payment.provider'].sudo().search([('code', '=', 'applepay')], limit=1)
#         if not provider:
#             return request.make_response(
#                 "Apple Pay provider configuration not found.",
#                 headers={'Content-Type': 'application/json'},
#                 status=400,
#             )
#
#         entity_id = provider.applepay_entity_id
#         authorization_bearer = provider.applepay_authorization_bearer
#
#         if not entity_id or not authorization_bearer:
#             return request.make_response(
#                 "Missing Apple Pay configuration. Ensure Entity ID and Authorization Token are set.",
#                 headers={'Content-Type': 'application/json'},
#                 status=400,
#             )
#
#         # Define headers for the API request
#         headers = {
#             'Authorization': f'Bearer {authorization_bearer}',
#             'Content-Type': 'application/x-www-form-urlencoded'
#         }
#
#         # Prepare payload for the request
#         payload = {
#             "entityId": entity_id,
#             "amount": amount,
#             "currency": currency,
#             "paymentType": payment_type,
#             "paymentBrand": payment_brand,
#             "card.number": card_number,
#             "card.expiryMonth": card_expiry_month,
#             "card.expiryYear": card_expiry_year,
#             "threeDSecure.verificationId": three_ds_verification_id,
#             "threeDSecure.eci": three_ds_eci,
#             "applePay.source": applepay_source,
#         }
#
#         # Make a call to the payment gateway
#         try:
#             response = request.post(
#                 url="https://eu-test.oppwa.com/v1/payments",
#                 headers=headers,
#                 data=payload  # Send payload directly as form-urlencoded
#             )
#             response_data = response.json()
#
#             # Return response based on the payment gateway result
#             if response.status_code == 200 and response_data.get('result', {}).get('code') == '000.100.110':
#                 return request.make_response(
#                     "Payment successful",
#                     headers={'Content-Type': 'application/json'},
#                     status=200,
#                 )
#             else:
#                 return request.make_response(
#                     f"Payment failed: {response_data.get('result', {}).get('description', 'Unknown error')}",
#                     headers={'Content-Type': 'application/json'},
#                     status=400,
#                 )
#         except Exception as e:
#             return request.make_response(
#                 f"An error occurred while processing the payment: {str(e)}",
#                 headers={'Content-Type': 'application/json'},
#                 status=500,
#             )
