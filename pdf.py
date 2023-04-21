from fpdf import FPDF

class PDF(FPDF):
    def setHeader(self, title):
        # Title
        self.set_font('ArialUnicodeMS', '', 20)
        self.multi_cell(0, 10, title, 'C')
        # Line break
        self.ln(20)
    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')