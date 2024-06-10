# caffe_module/models/report.py

from odoo import models, fields, api

class SaleReport(models.Model):
    _name = 'caffe.sale.report'
    _description = 'Laporan Penjualan'

    start_date = fields.Date(string='Tanggal Mulai', required=True)
    end_date = fields.Date(string='Tanggal Selesai', required=True)
    total_sales = fields.Float(string='Total Penjualan', compute='_compute_total_sales')

    @api.depends('start_date', 'end_date')
    def _compute_total_sales(self):
        for record in self:
            orders = self.env['caffe.pesanan'].search([
                ('order_date', '>=', record.start_date),
                ('order_date', '<=', record.end_date)
            ])
            total = sum(order.total_amount for order in orders)
            record.total_sales = total
