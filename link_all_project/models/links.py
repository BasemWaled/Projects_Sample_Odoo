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

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if not self.env.user.has_group('project.group_project_manager'):
            allowed_project_ids = self.env['project.project'].search([('user_access_ids', 'in', self.env.user.id)]).ids
            args += [('project_name_id', 'in', allowed_project_ids)]
        return super(LinkSystem, self).search(args, offset, limit, order, count)


# class LinkProject(models.Model):
#     _inherit = 'project.project'
#
#     user_access_ids = fields.Many2many('res.users', string='Project Employee', tracking=True)
#
#     @api.model
#     def search(self, args, offset=0, limit=None, order=None, count=False):
#         if not self.env.user.has_group('project.group_project_manager'):
#             args += [('user_access_ids', 'in', self.env.user.id)]
#         return super(LinkProject, self).search(args, offset, limit, order, count)


class LinkProject(models.Model):
    _inherit = 'project.project'

    user_access_ids = fields.Many2many('res.users', 'project_project_user_rel', 'project_id', 'user_id',
                                       string='Project Employees', tracking=True)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        # If the user is not an administrator and not a project manager
        if not self.env.user.has_group('base.group_system') and not self.env.user.has_group(
                'project.group_project_manager'):
            # Then restrict the projects to those in the user's project_access_ids field
            args += [('id', 'in', self.env.user.project_access_ids.ids)]
        return super(LinkProject, self).search(args, offset, limit, order, count)


class ResUsers(models.Model):
    _inherit = 'res.users'

    project_access_ids = fields.Many2many('project.project', 'project_project_user_rel', 'user_id', 'project_id',
                                          string='Accessible Projects')

# class LinkProject(models.Model):
#     _inherit = 'project.project'
#
#     user_access_ids = fields.Many2many('res.users', 'project_project_user_rel', 'project_id', 'user_id',
#                                        string='Project Employees', tracking=True)
#
#     @api.model
#     def search(self, args, offset=0, limit=None, order=None, count=False):
#         if not self.env.user.has_group('project.group_project_manager'):
#             args += [('user_access_ids', 'in', self.env.user.id)]
#         return super(LinkProject, self).search(args, offset, limit, order, count)
#     @api.model
#     def search(self, args, offset=0, limit=None, order=None, count=False):
#         if not self.env.user.has_group('project.group_project_manager') and self.env.user.has_group('base.group_user'):
#             args += [('user_access_ids', 'in', self.env.user.id)]
#         return super(LinkProject, self).search(args, offset, limit, order, count)
#
#
# class ResUsers(models.Model):
#     _inherit = 'res.users'
#
#     project_access_ids = fields.Many2many('project.project', 'project_project_user_rel', 'user_id', 'project_id',
#                                           string='Accessible Projects')
