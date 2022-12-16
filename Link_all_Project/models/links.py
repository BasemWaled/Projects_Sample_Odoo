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
    version = fields.Selection([('10','10'), ('11','11'),('12','12'), ('13','13'),('14','14'), ('15','15'),('16','16')], tracking=True)