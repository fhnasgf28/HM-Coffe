# caffe_module/models/pesanan.py

from odoo import models, fields, api

class Pesanan(models.Model):
    _name = 'caffe.pesanan'
    _description = 'Data Pesanan Pelanggan'

    name = fields.Char(string='Kode Pesanan', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))
    customer_name = fields.Char(string='Nama Pelanggan', required=True)
    order_date = fields.Datetime(string='Tanggal Pesanan', default=fields.Datetime.now)
    total_amount = fields.Float(string='Jumlah Total', required=True)
    order_line_ids = fields.One2many('caffe.pesanan.line', 'order_id', string='Detail Pesanan')
    waiter_id = fields.Many2one('caffe.pegawai', string='Pelayan', domain=[('job_position', '=', 'waiter')], required=True)

    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('caffe.pesanan') or ('New')
        result = super(Pesanan, self).create(vals)
        return result


class PesananLine(models.Model):
    _name = 'caffe.pesanan.line'
    _description = 'Detail Pesanan'

    order_id = fields.Many2one('caffe.pesanan', string='Kode Pesanan', required=True, ondelete='cascade')
    product_name = fields.Char(string='Nama Produk', required=True)
    quantity = fields.Integer(string='Kuantitas', required=True)
    price_unit = fields.Float(string='Harga Satuan', required=True)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
