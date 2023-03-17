from odoo import api, fields, models, _
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class Clinic_patient(models.Model):
    _name = 'clinic.patient'
    _description = 'Clinic Patient'

    @api.depends('date_of_birth')
    def onchange_age(self):
        for rec in self:
            if rec.date_of_birth:
                d1 = rec.date_of_birth
                d2 = datetime.today().date()
                rd = relativedelta(d2, d1)
                rec.age = str(rd.years) + "y" + " " + str(rd.months) + "m" + " " + str(rd.days) + "d"
            else:
                rec.age = "No Date Of Birth!!"

    patient_id = fields.Many2one('res.partner', string="Patient Name", required=True)
    ref = fields.Char(string='ID', readonly=True)
    date_of_birth = fields.Date(string="Date of Birth")
    sex = fields.Selection([('m', 'Male'), ('f', 'Female')], string="Sex")
    age = fields.Char(compute=onchange_age, string="Patient Age", store=True)
    mobile = fields.Char(related='patient_id.mobile', string='Mobile', tracking=True, readonly=False)
    critical_info = fields.Text(string="Patient Critical Information")
    image = fields.Binary(string="Picture")
    active = fields.Boolean(string='active', default=True)
    marital_status = fields.Selection(
        [('s', 'Single'), ('m', 'Married'), ('w', 'Widowed'), ('d', 'Divorced'), ('x', 'Seperated')],
        string='Marital Status')

    partner_address_id = fields.Many2one('res.partner', string="Address", )
    street = fields.Char(related='patient_id.street', readonly=False)
    street2 = fields.Char(related='patient_id.street2', readonly=False)
    zip_code = fields.Char(related='patient_id.zip', readonly=False)
    city = fields.Char(related='patient_id.city', readonly=False)
    state_id = fields.Many2one("res.country.state", related='patient_id.state_id', readonly=False)
    country_id = fields.Many2one('res.country', related='patient_id.country_id', readonly=False)

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('clinic.patient')
        return super(Clinic_patient, self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('clinic.patient')
        return super(Clinic_patient, self).write(vals)

    @api.constrains('date_of_death')
    def _check_date_death(self):
        for rec in self:
            if rec.date_of_birth:
                if rec.deceased == True:
                    if rec.date_of_death <= rec.date_of_birth:
                        raise UserError(_('Date Of Death Can Not Less Than Date Of Birth.'))

    def copy(self, default=None):
        for rec in self:
            raise UserError(_('You Can Not Duplicate Patient.'))
