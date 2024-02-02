# -*- coding: utf-8 -*-
# from odoo import http


# class PermohonanCuti(http.Controller):
#     @http.route('/permohonan_cuti/permohonan_cuti', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/permohonan_cuti/permohonan_cuti/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('permohonan_cuti.listing', {
#             'root': '/permohonan_cuti/permohonan_cuti',
#             'objects': http.request.env['permohonan_cuti.permohonan_cuti'].search([]),
#         })

#     @http.route('/permohonan_cuti/permohonan_cuti/objects/<model("permohonan_cuti.permohonan_cuti"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('permohonan_cuti.object', {
#             'object': obj
#         })
