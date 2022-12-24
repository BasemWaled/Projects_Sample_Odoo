from odoo import api, fields, models


class Linksystem(models.Model):
    _name = "project.links"
    _inherit = "project.project"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    project_Name = fields.Char(string='Project_Name', tracking=True)
    url = fields.Text(string='Url', tracking=True)
    userName = fields.Char(string='UserName', tracking=True)
    password = fields.Char(string='Password', tracking=True)
    project_Type = fields.Selection([('community', 'Community'), ('enterprise', 'Enterprise')], tracking=True)
    active = fields.Boolean(string='active', default=True)
    version = fields.Selection(
        [('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16')],
        tracking=True)
