# -*- coding: utf-8 -*-

import base64
import io
from odoo import models


class PatientCardXlsx(models.AbstractModel):
    _name = 'report.HM-Coffe.report_caffe_payroll_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
       print('method ini di klik')




