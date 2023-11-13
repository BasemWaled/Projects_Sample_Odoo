# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class HREmployeeInh(models.Model):
    _inherit = "hr.employee"

    emp_code =fields.Char(string='Employee code')
    enb_code =fields.Char(string='Bank Maser code')






