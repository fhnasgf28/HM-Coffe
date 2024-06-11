# caffe_module/models/pesanan.py

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Pesanan(models.Model):
    _name = 'caffe.pesanan'
    _description = 'Data Pesanan Pelanggan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string='Kode Pesanan', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: ('New'))
    customer_name = fields.Char(string='Nama Pelanggan', required=True)
    order_date = fields.Datetime(string='Tanggal Pesanan', default=fields.Datetime.now)
    total_amount = fields.Float(string='Jumlah Total', required=True, compute='_compute_total_amount')
    order_line_ids = fields.One2many('caffe.pesanan.line', 'order_id', string='Detail Pesanan')
    waiter_id = fields.Many2one('caffe.pegawai', string='Pelayan', domain=[('job_position', '=', 'waiter')],
                                required=True)
    invoice_id = fields.Many2one('account.move', string='faktur', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('caffe.pesanan') or ('New')
        result = super(Pesanan, self).create(vals)
        return result

    def action_confirm(self):
        for order in self:
            if order.invoice_id:
                raise UserError('faktur ini sudah dibuat')
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': self.env['res.partner'].search([('name', '=', order.customer_name)], limit=1).id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': [(0, 0, {
                    'product_id': line.product_name_id.id,
                    'quantity': line.quantity,
                    'price_unit': line.price_unit,
                }) for line in order.order_line_ids]
            }
            invoice = self.env['account.move'].create(invoice_vals)
            order.invoice_id = invoice.id

    @api.depends('order_line_ids.subtotal')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = sum(line.subtotal for line in order.order_line_ids)


class PesananLine(models.Model):
    _name = 'caffe.pesanan.line'
    _description = 'Detail Pesanan'

    order_id = fields.Many2one('caffe.pesanan', string='Kode Pesanan', required=True, ondelete='cascade')
    product_name_id = fields.Many2one('caffe.produk', string='Nama Produk', required=True)
    quantity = fields.Integer(string='Kuantitas', required=True)
    price_unit = fields.Float(string='Harga Satuan', required=True)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit

    def unlink(self):
        print('method ini diklik')
        for line in self:
            line.product_id.stock += line.quantity
        return super(PesananLine, self).unlink()

    # @api.model
    # def create(self, vals):
    #     product = self.env['caffe.product'].browse(vals['product_id'])
    #     if product.stock > vals['quantity']:
    #         raise ValidationError('Stok tidak mencukupi untuk produk: %s' % product.name)
    #     product.stock -= vals['quantity']
    #     return super(PesananLine, self).create(vals)
