# caffe_module/models/leave.py

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Leave(models.Model):
    _name = 'caffe.leave'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Cuti Pegawai'

    name = fields.Char(string='Nama Cuti', required=True)
    employee_id = fields.Many2one('caffe.pegawai', string='Pegawai', required=True)
    start_date = fields.Date(string='Tanggal Mulai', required=True)
    end_date = fields.Date(string='Tanggal Selesai', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak')
    ], string='Status', default='draft')

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        self.state = 'rejected'
