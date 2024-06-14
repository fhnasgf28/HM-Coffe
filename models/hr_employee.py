from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class Employee(models.Model):
    _inherit = 'hr.employee'
    _name = 'hr.employee'

    no_ktp = fields.Char(string='NIK')
    posisi = fields.Char(string='Posisi')