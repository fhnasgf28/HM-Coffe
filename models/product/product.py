# caffe_module/models/produk.py

from odoo import models, fields

class Produk(models.Model):
    _name = 'caffe.produk'
    _description = 'Data Produk Kafe'

    name = fields.Char(string='Nama Produk', required=True)
    category_id = fields.Many2one('caffe.produk.category', string='Kategori', required=True)
    price = fields.Float(string='Harga', required=True)
    stock = fields.Integer(string='Stok', required=True)

class ProdukCategory(models.Model):
    _name = 'caffe.produk.category'
    _description = 'Kategori Produk Kafe'

    name = fields.Char(string='Nama Kategori', required=True)
    product_ids = fields.One2many('caffe.produk', 'category_id', string='Produk')
