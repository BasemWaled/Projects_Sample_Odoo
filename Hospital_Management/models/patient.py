from odoo import api, fields, models
from datetime import date
from odoo.exceptions import ValidationError


class Hospitalpatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital patient"

    name = fields.Char(string='Name', tracking=True)
    date_of_birth = fields.Date(string='Date of Birth')
    mobile = fields.Char(string='Mobile', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True,
                              default='female')
    description = fields.Text(string='Description', tracking=True)
    ref = fields.Char(string='Internal Reference', tracking=True)
    active = fields.Boolean(string='active', default=True)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string='Tags')

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(Hospitalpatient, self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(Hospitalpatient, self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - (rec.date_of_birth.year + 1)
            else:
                rec.age = "No Date Of Birth!!"

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError('the Birthday you enter not allow ')
                return


class ModelName(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='color')
    color_2 = fields.Char(string='color 2')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_user_id = fields.Many2one('res.users', string="Confirm Users")

    def action_confirm(self):
        super(SaleOrder, self).action_confirm()
        print("Success..........")
        self.confirmed_user_id = self.env.user.id
