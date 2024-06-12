from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Shift(models.Model):
    _name = 'caffe.shift'
    _description = 'Jadwal Kerja Pegawai'

    name = fields.Char(string='Nama Shift', required=True)
    employee_id = fields.Many2one('caffe.pegawai', string='Pegawai', required=True)
    start_time = fields.Datetime(string='Waktu Mulai', required=True)
    end_time = fields.Datetime(string='Waktu Selesai', required=True)
    duration = fields.Float(string='Durasi (Jam)', compute='_compute_duration', store=True)

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for shift in self:
            if shift.start_time and shift.end_time:
                delta = shift.end_time - shift.start_time
                shift.duration = delta.total_seconds() / 3600
                if shift.duration > 12:
                    raise ValidationError("The shift duration cannot exceed 12 hours.")
                elif shift.duration < 0:
                    raise ValidationError("The shift duration cannot exceed 0 hours.")

    @api.constrains('start_time', 'end_time')
    def check_shift_time(self):
        for shift in self:
            if shift.start_time >= shift.end_time:
                raise ValidationError(_("Waktu Mulai Harus Lebih Kecil Dari Waktu Selesai"))

    @api.constrains('start_time', 'end_time', 'employee_id')
    def _check_shift_overlap(self):
        for shift in self:
            overlapping_shifts = self.env['caffe.shift'].search([
                ('employee_id', '=', shift.employee_id.id),
                ('id', '!=', shift.id),
                ('start_time', '<', shift.end_time),
                ('end_time', '>', shift.start_time),
            ])
            if overlapping_shifts:
                raise ValidationError('The Employee is already scheduled')
