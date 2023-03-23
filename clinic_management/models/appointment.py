from odoo import api, fields, models, _
# from datetime import datetime, date
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class clinic_appointment(models.Model):
    _name = 'clinic.appointment'
    _description = 'Medical Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Appointment ID", readonly=True, copy=True)
    patient_id = fields.Many2one('clinic.patient', string="Patient", required=True)
    doctor_id = fields.Many2one('res.partner', 'Doctor', required=True)
    appointment_date = fields.Datetime('Appointment Date', required=True, default=fields.Datetime.now)
    appointment_end = fields.Datetime('Appointment End', required=True)
    patient_status = fields.Selection(
        [('ambulatory', 'Ambulatory'), ('outpatient', 'Outpatient'), ('inpatient', 'Inpatient'), ], 'Patient status',
        sort=False, default='outpatient')
    validity_status = fields.Selection([('invoice', 'Invoice'), ('tobe', 'To be Invoiced'), ], 'Status', sort=False,
                                       readonly=True, default='tobe')
    comments = fields.Text(string="Info")
    state = fields.Selection(
        [('draft', 'Draft'), ('in_consultation', 'In Consultation'), ('done', 'Done'), ('cancel', 'Cancelled')],
        default='draft', string="Status", required=True, tracking=True)
    duration = fields.Integer('Duration')
    urgency_level = fields.Selection([('a', 'Normal'), ('b', 'Urgent'), ('c', 'Medical Emergency'), ], 'Urgency Level',
                                     sort=False, default="b")
    consultations_id = fields.Many2one('product.product', 'Consultation Service', required=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('clinic.appointment')
        return super(clinic_appointment, self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['name'] = self.env['ir.sequence'].next_by_code('clinic.appointment')
        return super(clinic_appointment, self).write(vals)

    def create_invoice(self):
        lab_req_obj = self.env['clinic.appointment']
        account_invoice_obj = self.env['account.invoice']
        account_invoice_line_obj = self.env['account.invoice.line']

        lab_req = lab_req_obj
        if lab_req.is_invoiced == True:
            raise UserError(_(' Invoice is Already Exist'))
        if lab_req.no_invoice == False:
            res = account_invoice_obj.create(
                {'partner_id': lab_req.patient_id.patient_id.id, 'date_invoice': date.today(),
                 'account_id': lab_req.patient_id.patient_id.property_account_receivable_id.id, })

            res1 = account_invoice_line_obj.create(
                {'product_id': lab_req.consultations_id.id, 'product_uom': lab_req.consultations_id.uom_id.id,
                 'name': lab_req.consultations_id.name, 'product_uom_qty': 1,
                 'price_unit': lab_req.consultations_id.lst_price,
                 'account_id': lab_req.patient_id.patient_id.property_account_receivable_id.id, 'invoice_id': res.id})

            if res:
                lab_req.write({'is_invoiced': True})
                imd = self.env['ir.model.data']
                action = self.env.ref('account.action_invoice_tree1')
                list_view_id = imd.sudo()._xmlid_to_res_id('account.view_order_form')
                result = {'name': action.name, 'help': action.help, 'type': action.type,
                          'views': [[list_view_id, 'form']], 'target': action.target, 'context': action.context,
                          'res_model': action.res_model, 'res_id': res.id, }
                if res:
                    result['domain'] = "[('id','=',%s)]" % res.id
        else:
            raise UserError(_(' The Appointment is invoice exempt'))
        return result

    def action_in_consultation(self):
        for rec in self:
            rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    # def action_cancel(self):
    #     action = self.env.ref('clinic_management.action_cancel_appointment').read()[0]
    #     return action
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
