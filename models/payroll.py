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

    @api.depends('total_hours', 'hourly_rate')
    def _compute_total_hours(self):
        for payroll in self:
            shifts = self.env['caffe.shift'].search([
                ('employee_id', '=', payroll.employee_id.id),
                ('start_time', '>=', payroll.date_from),
                ('end_time', '<=', payroll.date_to),
            ])
            payroll.total_hours = sum(shift.duration for shift in shifts)

    @api.depends('total_hours', 'hourly_rate')
    def _compute_total_salary(self):
        for payroll in self:
            payroll.total_salary = payroll.total_hours * payroll.hourly_rate

