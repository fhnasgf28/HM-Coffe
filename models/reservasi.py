# caffe_module/models/reservasi.py
from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api

class Reservasi(models.Model):
    _name = 'caffe.reservasi'
    _description = 'Reservasi Meja'

    customer_name = fields.Char(string='Nama Pelanggan', required=True)
    reservation_date = fields.Datetime(string='Tanggal Reservasi', required=True)
    table_number = fields.Integer(string='Nomor Meja', required=True)
    number_of_people = fields.Integer(string='Jumlah Orang', required=True)
    status = fields.Selection([('reserved', 'Reserved'), ('completed', 'Completed'), ('canceled', 'Canceled')], string='Status', default='reserved')

    @api.model
    def create(self, vals):
        if self.search([('table_number', '=', vals['table_number']), ('reservation_date', '=', vals['reservation_date']), ('status', '=', 'reserved')]):
            raise ValidationError('Meja ini sudah dipesan pada waktu tersebut.')
        return super(Reservasi, self).create(vals)
