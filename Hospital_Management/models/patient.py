from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital patient"

    name = fields.Char(string='Name', tracking=True)
    date_of_birth = fields.Date(string='Date of Birth')
    mobile = fields.Char(string='Mobile', tracking=True, size=11)
    age = fields.Integer(string='Age', compute='_compute_age', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True,
                              default='female')
    description = fields.Text(string='Description', tracking=True)
    ref = fields.Char(string='Internal Reference', tracking=True)
    active = fields.Boolean(string='active', default=True)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string='Tags')
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointment")

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - (rec.date_of_birth.year + 1)
            else:
                rec.age = 1

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError('The Birthday you enter not allow ')

    # def name_get(self):
    #     patient_list = []
    #     for rec in self:
    #         name = str(rec.ref) + ' ' + rec.name
    #         patient_list.append((rec.id, name))
    #     return patient_list
    def name_get(self):
        return [(rec.id, "[%s] %s" % (rec.ref, rec.name)) for rec in self]


class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='color')
    color_2 = fields.Char(string='color 2')
    sequence = fields.Integer(string="Sequence")

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}

        if not default.get('name'):
            default["name"] = _("%s (copy)", self.name)
        return super(PatientTag, self).copy(default)

    sql_constraints = [
        ('unique_tag_name', 'unique (name, active)', 'Name must be unique.'),
        ('check_sequence', 'check (sequence > 0)', 'sequence must be non zero positive number.')
    ]


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_user_id = fields.Many2one('res.users', string="Confirm Users")

    def action_confirm(self):
        super(SaleOrder, self).action_confirm()
        print("Success..........")
        self.confirmed_user_id = self.env.user.id
