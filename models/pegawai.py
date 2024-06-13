# caffe_module/models/pegawai.py

from odoo import models, fields, api
from odoo.modules.module import get_module_resource
import base64


class Pegawai(models.Model):
    _name = 'caffe.pegawai'
    _description = 'Data Pegawai Kafe'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    name = fields.Char(string='Nama', required=True)
    employee_id = fields.Char(string='ID Pegawai', required=True, copy=False, readonly=True, index=True,
                              default=lambda self: ('New'))
    hourly_rate = fields.Float(string='Tarif per Jam', required=True)
    shift_ids = fields.One2many('caffe.shift', 'employee_id', string='Shifts')
    leave_ids = fields.One2many('caffe.leave', 'employee_id', string='Cuti')
    job_position = fields.Selection([
        ('manager', 'Manager'),
        ('barista', 'Barista'),
        ('chef', 'Chef'),
        ('waiter', 'Waiter')
    ], string='Posisi', required=True)
    date_of_birth = fields.Date(string='Tanggal Lahir')
    hire_date = fields.Date(string='Tanggal Bergabung', default=fields.Date.context_today)
    email = fields.Char(string='Email')
    address = fields.Text(string='Alamat')
    image_1920 = fields.Image(default=_default_image)
    #private information
    address_home_id = fields.Many2one(
        'res.partner', 'Address',
        help='Enter here the private address of the employee, not the one linked to your company.',options='{"always_reload": True, "highlight_first_line": True}',
         tracking=True)
    private_email = fields.Char(related='address_home_id.email', string="Private Email")
    phone = fields.Char(related='address_home_id.phone', related_sudo=False, readonly=False, string="Private Phone")
    km_home_work = fields.Integer(string="Home-Work Distance", tracking=True)
    children = fields.Integer(string='Number of Children', tracking=True)
    emergency_contact = fields.Char("Emergency Contact", tracking=True)
    emergency_phone = fields.Char("Emergency Phone", tracking=True)
    certificate = fields.Selection([
        ('graduate', 'Graduate'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('doctor', 'Doctor'),
        ('other', 'Other'),
    ], 'Certificate Level', default='other', tracking=True)
    study_field = fields.Char("Field of Study", tracking=True)
    study_school = fields.Char("School", tracking=True)
    # citizenship
    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)', tracking=True)
    identification_id = fields.Char(string='Identification No', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], tracking=True)
    birthday = fields.Date('Date of Birth', tracking=True)
    place_of_birth = fields.Char('Place of Birth', tracking=True)
    country_of_birth = fields.Many2one('res.country', string="Country of Birth", tracking=True)











    _sql_constraints = [
        ('unique_employee_id_name', 'UNIQUE(name)', 'names must be unique')
    ]

    @api.model
    def create(self, vals):
        if vals.get('employee_id', ('New')) == ('New'):
            vals['employee_id'] = self.env['ir.sequence'].next_by_code('caffe.pegawai') or ('New')
        result = super(Pegawai, self).create(vals)
        return result
