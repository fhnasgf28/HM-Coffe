from odoo import models, fields, api

class Payroll(models.Model):
    _name = 'caffe.payroll'
    _description = 'Penggajian Pegawai'

    employee_id = fields.Many2one('caffe.pegawai', string='Pegawai', required=True)
    date_from = fields.Date(string='Dari Tanggal', required=True)
    date_to = fields.Date(string='Sampai Tanggal', required=True)
    total_hours = fields.Float(string='Total Jam Kerja', compute='_compute_total_hours', store=True)
    hourly_rate = fields.Float(string='Tarif per Jam', related='employee_id.hourly_rate')
    total_salary = fields.Float(string='Total Gaji', compute='_compute_total_salary', store=True)

    def _compute_total_hours(self):
        pass

    def _compute_total_salary(self):
        pass

