import io

from odoo import http
from odoo.http import content_disposition, request
import xlsxwriter
import datetime

class ReportExcelEstateController(http.Controller):
    @http.route(['/estate/estate_report_excel/<model("estate.property"):data>', ], type='http', auth="user", csrf=False)
    def get_report_excel_report(self, data=None, **args):
        response = request.make_response(
            None,
            headers = [
                ('Content_Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', content_disposition('Estate Report' + '.xlsx'))
            ]
        )

        #create object from library xlswriter
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory':True})

        # setting style
        top_style = workbook.add_format({'font_name': 'Times', 'bold': True, 'align': 'left'})
        top_isi_style = workbook.add_format({'font_name': 'Times', 'bold':False, 'align':'left'})
        header_style = workbook.add_format(
            {'font_name': 'Times', 'bold': True, 'left':1, 'bottom': 1, 'top':1, 'right':1, 'align': 'center'})
        text_style = workbook.add_format(
            {'font_name': 'Times', 'bold': False, 'left': 1, 'bottom': 1, 'top': 1, 'right': 1, 'align': 'left'}
        )

#         looping data yang mau pilih
        for top in data:
            #worksheet/ tap ber user
            sheet = workbook.add_worksheet(top.name)
            #set orientasi landscape
            sheet.set_landscape()
            #set ukuran /size kertas
            sheet.set_paper(9)

            #set margin
            sheet.set_margins(0.5, 0.5, 0.5)
            #atur lebar kolom
            sheet.set_column('A:A', 5)
            sheet.set_column('B:B', 50)
            sheet.set_column('C:C', 50)
            sheet.set_column('D:D', 10)
            sheet.set_column('E:E', 10)
            sheet.set_column('F:F', 10)

            #ATUR JUDUL
            sheet.merge_range('A1:B1', 'Name', top_style)
            sheet.merge_range('A2:B2', 'Tanggal', top_style)

            #atur isi judul
            sheet.write(1, 2, top.name, top_isi_style)
            tanggal = top.date_availability
            sheet.write(1, 2, tanggal.strftime("%d%m%Y"), top_isi_style)

            #atur judul kolom
            sheet.write(3, 0, 'No', header_style)
            sheet.write(3, 0, 'Title', header_style)
            sheet.write(3, 1, 'Post Code', header_style)

            row = 4
            number = 1

            #mencari record dari autidak yang akan ditampilkan

            record_line = request.env['estate.property'].search([('property_type_id', '=', top.id)])
            for record in record_line:
                #isi dari tabel
                sheet.write(row, 0, number, text_style)
                sheet.write(row, 1, record.name, text_style)
                sheet.write(row, 2, record.description, text_style)

                row += 1
                number += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
        return response

