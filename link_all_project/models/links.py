from odoo import api, fields, models


class LinkSystem(models.Model):
    _name = "project.links"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    project_name_id = fields.Many2one('project.project', string='Project Name', tracking=True, required=True)
    url = fields.Text(string='Url', tracking=True, required=True)
    userName = fields.Char(string='UserName', tracking=True, required=True)
    password = fields.Char(string='Password', tracking=True, required=True)
    project_Type = fields.Selection([('community', 'Community'), ('enterprise', 'Enterprise')], tracking=True,
                                    required=True)
    active = fields.Boolean(string='active', default=True)
    version = fields.Selection(
        [('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16')],
        tracking=True, required=True)
