# caffe_module/models/produk.py

from odoo import models, fields

class Produk(models.Model):
    _name = 'caffe.produk'
    _description = 'Data Produk Kafe'

    name = fields.Char(string='Nama Produk', required=True)
    category_id = fields.Many2one('caffe.produk.category', string='Kategori', required=True)
    price = fields.Float(string='Harga', required=True)
    low_stock_threshold = fields.Integer(string='Ambang Batas Stok Rendah', default=10)
    stock = fields.Integer(string='Stok', required=True)
    supplier_id = fields.Many2one('res.partner', string='Pemasok', required=True)

    def check_and_order_stock(self):
        print('method ini diklik')
        for product in self:
            if product.stock < product.low_stock_threshold:
                self._create_purchase_order(product)

    def _create_purchase_order(self, product):
        purchase_order_vals = {
            'partner_id': product.supplier_id.id,
            'date_order': fields.Datetime.now(),
            'order_line': [(0, 0, {
                'product_id': product.id,
                'product_qty': product.low_stock_threshold * 2,  # Contoh pesanan: dua kali ambang batas stok rendah
                'price_unit': product.price,
                'date_planned': fields.Datetime.now(),
            })]
        }
        self.env['purchase.order'].create(purchase_order_vals)


class ProdukCategory(models.Model):
    _name = 'caffe.produk.category'
    _description = 'Kategori Produk Kafe'

    name = fields.Char(string='Nama Kategori', required=True)
    product_ids = fields.One2many('caffe.produk', 'category_id', string='Produk')
