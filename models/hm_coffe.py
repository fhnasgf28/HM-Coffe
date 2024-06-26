from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class HashmicroProduct(models.Model):
    _name = 'hashmicro.coffe'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'hasmicro coffe'

    PRODUCTFAZ_SELECTION = [
        ('coffe_arabica', 'Kopi Arabika'),
        ('coffe_robusta', 'Kopi Robusta'),
        ('coffe_liberika', 'Kopi Liberika'),
    ]

    name = fields.Char(string='hashmicro', default=lambda self: _('New'), copy=False, readonly=True, tracking=True,
                       index=True)
    partner_id = fields.Many2one('res.partner', string='Vendor')
    category = fields.Selection(PRODUCTFAZ_SELECTION, string='Category', default='coffe_arabica')
    description = fields.Char(string='Descriptions')
    order_deadline = fields.Datetime(string='Order Deadline', default=fields.Datetime.now())
    product_names = fields.Char(string='Product Names')
    user_id = fields.Many2one('res.users', string='User', index=True)
    product_line_ids = fields.One2many('caffe.produk', 'product_id', string='Detail Pesanan')
    uom_qty = fields.Float(string="Quantity", default=1,
                           help="The quantity converted into the UoM used by "
                                "the product")
    invoice_id = fields.Many2one('account.move', string='Invoice', domain="[('type', '=', 'out_invoice')]")
    curency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.ref('base.IDR'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancel', 'canceled'),
        ('done', 'Done'),
    ], string='Status', default='draft')
    phone = fields.Char(string="Phone", default=62)

    def action_refresh_price(self):
        pass

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_send_whatsapp(self):
        pass

    def action_whatsapp_multi(self):
        pass

    @api.constrains('uom_qty')
    def quantity_constrains(self):
        for quantity in self:
            if quantity.uom_qty < 0:
                raise ValidationError(_('quantity cannot be Negative'))

    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hashmicro.coffe') or ('New')
        result = super(HashmicroProduct, self).create(vals)
        return result