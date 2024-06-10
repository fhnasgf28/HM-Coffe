from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class HashmicroProduct(models.Model):
    _name = 'hashmicro.coffe'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'hasmicro coffe'

    PRODUCTFAZ_SELECTION = [
        ('consumable', 'Consumable'),
        ('service', 'Service'),
        ('storable', 'Storable Product'),
    ]

    name = fields.Char(string='hashmicro', default=lambda self: _('New'), copy=False, readonly=True, tracking=True,
                       index=True)
    partner_id = fields.Many2one('res.partner', string='Vendor')
    category = fields.Selection(PRODUCTFAZ_SELECTION, string='Category', default='consumable')
    description = fields.Char(string='Descriptions')
    order_deadline = fields.Datetime(string='Order Deadline', default=fields.Datetime.now())
    product_names = fields.Char(string='Product Names')
    user_id = fields.Many2one('res.users', string='User', index=True)
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
    ], string='Status', readonly=True, default='draft')
    phone = fields.Char(string="Phone", default=62)

    def action_refresh_price(self):
        pass

    def action_confirm(self):
        pass

    def action_draft(self):
        pass

    def action_done(self):
        pass

    def action_send_whatsapp(self):
        pass

    def action_whatsapp_multi(self):
        pass


