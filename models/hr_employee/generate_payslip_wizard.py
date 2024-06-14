from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class GeneratePayslipWizard(models.TransientModel):
    _name = 'generate.payslip.wizard'
    _description = 'Generate Payslip Wizard'

    payroll_id = fields.Many2one('caffe.payroll', "Payroll")
    period = fields.Char(related='payroll_id.period')
    type = fields.Selection([
        ('all', 'All Employee'),
        ('specific', 'Specific Employee')
    ], default='all', required=1)
    employee_ids = fields.Many2many('caffe.pegawai', string='Employees')
    available_days_of_work = fields.Integer(related='payroll_id.available_days_of_work')

    def confirm(self):
        pass