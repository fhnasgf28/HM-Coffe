# -*- coding: utf-8 -*-
{
    'name': "HM-coffee",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product', 'stock', 'purchase', 'account', 'sale','mail','hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/hm_coffe_views.xml',
        'views/pegawai_views.xml',
        'views/pesanan_views.xml',
        'views/report/report_views.xml',
        'views/product/product_views.xml',
        'views/loyalitas_pelanggan_views.xml',
        'views/payroll_views.xml',
        'views/performance_review_view.xml',
        'views/shift_views.xml',
        'views/leave_views.xml',
        'views/reservasi_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
