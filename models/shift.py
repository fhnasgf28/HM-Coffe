from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Shift(models.Model):
    _name = 'caffe.shift'
    _description = 'Jadwal Kerja Pegawai'

    name = fields.Char(string='Nama Shift', required=True)
    employee_id = fields.Many2one('caffe.pegawai', string='Pegawai', required=True)
    start_time = fields.Datetime(string='Waktu Mulai', required=True)
    end_time = fields.Datetime(string='Waktu Selesai', required=True)
    duration = fields.Float(string='Durasi (Jam)', compute='_compute_duration', store=True)

    def _compute_duration(self):
        pass