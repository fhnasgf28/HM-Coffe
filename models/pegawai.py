# caffe_module/models/pegawai.py

from odoo import models, fields, api


class Pegawai(models.Model):
    _name = 'caffe.pegawai'
    _description = 'Data Pegawai Kafe'

    name = fields.Char(string='Nama', required=True)
    employee_id = fields.Char(string='ID Pegawai', required=True, copy=False, readonly=True, index=True,
                              default=lambda self: ('New'))
    hourly_rate = fields.Float(string='Tarif per Jam', required=True)
    shift_ids = fields.One2many('caffe.shift', 'employee_id', string='Shifts')
    leave_ids = fields.One2many('caffe.leave', 'employee_id', string='Cuti')
    job_position = fields.Selection([
        ('manager', 'Manager'),
        ('barista', 'Barista'),
        ('chef', 'Chef'),
        ('waiter', 'Waiter')
    ], string='Posisi', required=True)
    date_of_birth = fields.Date(string='Tanggal Lahir')
    hire_date = fields.Date(string='Tanggal Bergabung', default=fields.Date.context_today)
    phone = fields.Char(string='Telepon')
    email = fields.Char(string='Email')
    address = fields.Text(string='Alamat')
    image = fields.Binary(string='Foto')

    @api.model
    def create(self, vals):
        if vals.get('employee_id', ('New')) == ('New'):
            vals['employee_id'] = self.env['ir.sequence'].next_by_code('caffe.pegawai') or ('New')
        result = super(Pegawai, self).create(vals)
        return result
