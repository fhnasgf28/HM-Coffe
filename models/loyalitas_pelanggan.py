# caffe_module/models/loyalty.py

from odoo import models, fields, api

class CustomerLoyalty(models.Model):
    _name = 'caffe.loyalty'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Loyalitas Pelanggan'

    customer_name = fields.Char(string='Nama Pelanggan', required=True)
    points = fields.Integer(string='Poin', default=0)

class Pesanan(models.Model):
    _inherit = 'caffe.pesanan'

    @api.model
    def create(self, vals):
        order = super(Pesanan, self).create(vals)
        loyalty = self.env['caffe.loyalty'].search([('customer_name', '=', order.customer_name)], limit=1)
        if not loyalty:
            loyalty = self.env['caffe.loyalty'].create({'customer_name': order.customer_name})
        loyalty.points += int(order.total_amount / 10)  # 1 point for every 10 units of currency
        return order
