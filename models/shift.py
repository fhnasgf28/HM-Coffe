from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime


class Shift(models.Model):
    _name = 'caffe.shift'
    _description = 'Jadwal Kerja Pegawai'

    name = fields.Char(string='Nama Shift', required=True)
    employee_id = fields.Many2one('caffe.pegawai', string='Pegawai', required=True)
    start_time = fields.Date(string='Waktu Mulai', readonly=True)
    end_time = fields.Datetime(string='Waktu Selesai')
    duration = fields.Integer(string='Durasi (Jam)', store=True)
    total_hours = fields.Float(string="Total Hours Worked", compute='_compute_total_hours', store=True)
    total_shift = fields.Float(string='Total Shift', compute='_compute_total_shift', store=True, readonly=True)
    schedule_line_ids = fields.One2many('employee.schedule.line', 'schedule_id', string="Schedule Lines")

    # @api.depends('start_time', 'end_time')
    # def _compute_duration(self):
    #     for shift in self:
    #         if shift.start_time and shift.end_time:
    #             delta = shift.end_time - shift.start_time
    #             shift.duration = delta.total_seconds() / 3600
    #             if shift.duration > 12:
    #                 raise ValidationError("The shift duration cannot exceed 12 hours.")
    #             elif shift.duration < 0:
    #                 raise ValidationError("The shift duration cannot exceed 0 hours.")
    @api.depends('schedule_line_ids.hours_worked')
    def _compute_total_hours(self):
        for schedule in self:
            total_hours = sum(line.hours_worked for line in schedule.schedule_line_ids)
            schedule.total_hours = total_hours

    @api.constrains('start_time', 'end_time')
    def check_shift_time(self):
        for shift in self:
            if shift.start_time >= shift.end_time:
                raise ValidationError(_("Waktu Mulai Harus Lebih Kecil Dari Waktu Selesai"))

    @api.depends('start_time')
    def _onchange_date_hours_worked(self):
        print('method ini di klik')
        for shift in self:
            if shift.start_time and shift.total_hours:
                shift.end_time = shift.start_time + timedelta(hours=shift.total_hours)

    @api.constrains('start_time', 'end_time', 'employee_id')
    def _check_shift_overlap(self):
        for shift in self:
            overlapping_shifts = self.env['caffe.shift'].search([
                ('employee_id', '=', shift.employee_id.id),
                ('id', '!=', shift.id),
                ('start_time', '<', shift.end_time),
                ('end_time', '>', shift.start_time),
            ])
            if overlapping_shifts:
                raise ValidationError('The Employee is already scheduled')

    @api.depends('schedule_line_ids')
    def _compute_total_shift(self):
        for shift in self:
            shift.total_shift = len(shift.schedule_line_ids)


class EmployeeScheduleLine(models.Model):
    _name = 'employee.schedule.line'
    _description = 'Employee Schedule Line'

    schedule_id = fields.Many2one('caffe.shift', string="Employee Schedule", required=True, ondelete='cascade')
    date = fields.Datetime(string="Waktu Mulai", required=True)
    hours_worked = fields.Float(string="Hours Worked", compute='_compute_hours_worked', store=True, readonly=True)
    end_time = fields.Datetime(string='Waktu Selesai', required=True)

    @api.depends('date', 'end_time')
    def _compute_hours_worked(self):
        for line in self:
            if line.date and line.end_time:
                start_time = fields.Datetime.from_string(line.date)
                end_time = fields.Datetime.from_string(line.end_time)
                delta = end_time - start_time
                line.hours_worked = delta.total_seconds() / 3600
                if line.hours_worked < 1:
                    raise ValidationError(_("Total working hours cannot be less than 1 hour."))

    @api.constrains('date')
    def _check_date(self):
        for line in self:
            if line.date:
                current_time = fields.Datetime.now()
                if line.date < current_time:
                    raise ValidationError(
                        _('The Date and time must be in the future. Please select a date and time that is not in the past.'))

    @api.constrains('end_time')
    def _check_end_time(self):
        for line in self:
            if line.date and line.end_time:
                if line.end_time < line.date:
                    raise ValidationError(_("End time cannot be before start time."))

    @api.onchange('date', 'end_time')
    def _onchange_hours_worked(self):
        if self.date and self.end_time:
            start_time = fields.Datetime.from_string(self.date)
            end_time = fields.Datetime.from_string(self.end_time)
            delta = end_time - start_time
            hours_worked = delta.total_seconds() / 3600
            if hours_worked > 7:
                self.date = False
                self.end_time = False
                return {
                    'warning': {
                        'title': _('Validation Error'),
                        'message': _('Total Working hours cannot exceed 7 hours. Please adjust the start and end time.')
                    }
                }
