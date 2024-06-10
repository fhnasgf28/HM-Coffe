# -*- coding: utf-8 -*-
# from odoo import http


# class Hm-coffee(http.Controller):
#     @http.route('/hm-coffee/hm-coffee/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hm-coffee/hm-coffee/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hm-coffee.listing', {
#             'root': '/hm-coffee/hm-coffee',
#             'objects': http.request.env['hm-coffee.hm-coffee'].search([]),
#         })

#     @http.route('/hm-coffee/hm-coffee/objects/<model("hm-coffee.hm-coffee"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hm-coffee.object', {
#             'object': obj
#         })
