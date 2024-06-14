from odoo import models, fields, api, _


class Payroll(models.Model):
    _name = 'caffe.payroll'
    _description = 'Penggajian Pegawai'

    name = fields.Char(string='Number', required=1, index=True, default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('release', 'Released'),
        ('confirm', 'Confirmed')
    ], default='draft', required=1, copy=0)
    employee_id = fields.Many2one('caffe.pegawai', string='Pegawai', required=True)
    date_from = fields.Date(string='Dari Tanggal', required=True)
    date_to = fields.Date(string='Sampai Tanggal', required=True)
    total_hours = fields.Float(string='Total Jam Kerja', compute='_compute_total_hours', store=True)
    hourly_rate = fields.Float(string='Tarif per Jam', related='employee_id.hourly_rate')
    total_salary = fields.Float(string='Total Gaji', compute='_compute_total_salary', store=True)

    period = fields.Char(compute='_get_period')
    payslip_ids = fields.One2many('payslip', 'payroll_id', string='Payslip', copy=True, auto_join=True)
    amount_total = fields.Monetary(string='Total', currency_field='currency_id', compute='get_amount')
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company, required=1)
    currency_id = fields.Many2one(related='company_id.currency_id', depends=["company_id"], store=1,
                                  ondelete="restrict")
    available_days_of_work = fields.Integer(string="Jumlah Masuk",)
    from_date = fields.Date(required=1)
    to_date = fields.Date(required=1)

    @api.depends('total_hours', 'hourly_rate')
    def _compute_total_hours(self):
        for payroll in self:
            shifts = self.env['caffe.shift'].search([
                ('employee_id', '=', payroll.employee_id.id),
                ('start_time', '>=', payroll.date_from),
                ('end_time', '<=', payroll.date_to),
            ])
            payroll.total_hours = sum(shift.duration for shift in shifts)

    @api.depends('total_hours', 'hourly_rate')
    def _compute_total_salary(self):
        for payroll in self:
            payroll.total_salary = payroll.total_hours * payroll.hourly_rate

    #     new
    def get_amount(self):
        pass

    def _get_period(self):
        pass

    def confirm(self):
        self.state = 'confirm'

    def generate_payslip(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Generate Payslip Wizard"),
            "res_model": "generate.payslip.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {},
        }

class Payslip(models.Model):
    _name = 'payslip'
    _description = 'Payslip'
    _rec_name = 'name'

    payroll_id = fields.Many2one('caffe.payroll', required=True, ondelete='cascade', index=True, copy=False)
    period = fields.Char(related='payroll_id.period')
    name = fields.Char(string='Payslip Number', required=1, index=1, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Name', index=1)
    no_ktp = fields.Char(related='employee_id.no_ktp')
    jabatan = fields.Char(related='employee_id.posisi')
    jumlah_masuk = fields.Integer()
    absen = fields.Integer()
    ijin = fields.Integer()
    sakit = fields.Integer()
    absen_weekend = fields.Integer()
    ijin_weekend = fields.Integer()
    sakit_weekend = fields.Integer()
    salary = fields.Monetary(currency_field='currency_id')
    deduction = fields.Monetary(currency_field='currency_id')
    allowance = fields.Monetary(currency_field='currency_id')
    overtime = fields.Monetary(currency_field='currency_id')
    incentive = fields.Monetary(currency_field='currency_id')
    other_deduction = fields.Monetary(currency_field='currency_id')
    gross_salary = fields.Monetary(string='Gross Salary', currency_field='currency_id')
    thp = fields.Monetary(string='THP', currency_field='currency_id')
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company, required=1)
    currency_id = fields.Many2one(related='company_id.currency_id', depends=["company_id"], store=1,
                                  ondelete="restrict")
    available_days_of_work = fields.Integer(string="Jumlah Masuk")

    def _get_thp(self):
        pass

    def print(self):
        print('method ini diklik')
        return self.env.ref('HM-Coffe.action_payslip_report_farhan').report_action(self, data=None)