from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"
    _description = "crm_inh"

    # phone_number = fields.Char(compute='_compute_phone_number', string='Phone Number')

    # @api.depends('partner_id.phone')
    # def _compute_phone_number(self):
    #     for lead in self:
    #         lead.phone_number = lead.partner_id.phone or ''

    def whatsAppLoop(self):
        print("Button Clicked !!!!!!")

# from werkzeug.utils import redirect
# from odoo import api, fields, models
#
#
# class CrmLead(models.Model):
#     _inherit = "crm.lead"
#     _description = "crm_inh"
#
#     def whatsAppLoop(self):
#         phone_number = self.partner_id.phone
#         print(phone_number)
#         url = "https://wa.me/{}".format(phone_number)
#         return redirect(url)
# #
