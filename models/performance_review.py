# caffe_module/models/performance_review.py

from odoo import models, fields, api

class PerformanceReview(models.Model):
    _name = 'caffe.performance_review'
    _description = 'Evaluasi Kinerja Pegawai'

    employee_id = fields.Many2one('caffe.pegawai', string='Pegawai', required=True)
    date = fields.Date(string='Tanggal Evaluasi', required=True)
    reviewer_id = fields.Many2one('res.users', string='Penilai', required=True, default=lambda self: self.env.user)
    rating = fields.Selection([
        ('1', 'Sangat Buruk'),
        ('2', 'Buruk'),
        ('3', 'Cukup'),
        ('4', 'Baik'),
        ('5', 'Sangat Baik')
    ], string='Penilaian', required=True)
    comments = fields.Text(string='Komentar')

    @api.model
    def create(self, vals):
        review = super(PerformanceReview, self).create(vals)
        # Tambahan logika jika diperlukan
        return review
