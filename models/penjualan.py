from odoo import models, fields, api

class Penjualan(models.Model):
    _name = 'hmcoffe.penjualan'
    _description = 'mode.technical.name'

    name = fields.Char(string='nama')
    tgl_transaksi = fields.Datetime(string='Tanggal Transaksi', default=fields.Datetime.now())
    detail_penjualan_ids = fields.One2Many('hmcoffee.detailpenjualan', 'penjua')


class DetailPenjualan(models.Model):
    _name = 'hmcoffee.detailpenjualan'
    _description = 'detail penjualan'

    penjualan_id = fields.Many2one('hmcoffee.penjualan', string='Penjualan')
    bahan_id = fields.Many2one('hmcoffee.bahan', string='Barang')
    harga_satuan = fields.Integer(compute='_compute_harga_satuan',)
