from odoo import api, fields, models


class Linksystem(models.Model):
    _name = "project.name"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    Project_Name = fields.Char(string='Project_Name', tracking=True)
    Url = fields.Text(string='Url', tracking=True)
    UserName = fields.Char(string='UserName', tracking=True)
    Password = fields.Char(string='Password', tracking=True)
    Project_Type = fields.Selection([('community', 'Community'), ('enterprise', 'Enterprise')], tracking=True)
    active = fields.Boolean(string='active', default=True)
