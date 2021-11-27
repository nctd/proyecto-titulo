
from fpdf import FPDF, HTMLMixin

class PDF(FPDF, HTMLMixin):
    def titles(self,title):
        self.set_xy(14,0)
        self.set_font('Arial', 'B', 12)
        self.cell(100, 40, align='L', txt=title, border=False)
        
    def texto(self,text,x,y):
        self.set_xy(x,y)    
        self.set_font('Arial', 'I', 8)
        self.cell(120,40,text)
        
        
    def linea(self):
        self.set_line_width(0.5)
        self.set_draw_color(103, 131, 179)
        self.line(10, 25, 195, 25)
        self.line(10, 75, 195, 75)
        # X inicio, Y inicio, X fin, Y termino
    

    def tabla(self, headings, rows, col_widths=(30, 20, 85, 20, 30)):
        # Colors, line width and bold font: 
        self.set_y(80)
        self.set_fill_color(217, 226, 243)
        self.set_text_color(0)
        self.set_draw_color(255, 255, 255)
        self.set_line_width(0.3)
        self.set_font('Arial', 'B', 8)
        for col_width, heading in zip(col_widths, headings):
            self.cell(col_width, 7, heading, 1, 0, "C", True)
        self.ln()
        # Color and font restoration:
        self.set_fill_color(217, 226, 243)
        self.set_text_color(0)
        self.set_font('Arial', '', 6)
        fill = True
        for row in rows:
            self.cell(col_widths[0], 6, row[0], "TLRB", 0, 'C', fill)
            self.cell(col_widths[1], 6, row[1], "TLRB", 0, "C", fill)
            self.cell(col_widths[2], 6, row[2], "TLRB", 0, "C", fill)
            self.cell(col_widths[3], 6, row[3], "TLRB", 0, "C", fill)
            self.cell(col_widths[4], 6, row[4], "TLRB", 0, "C", fill)
            self.ln()
            # fill = not fill
        self.cell(sum(col_widths), 0, "", "T")
        
    def tabla_PL(self, headings, rows,totales, col_widths=(25, 15, 55, 15, 15,15,15,15,15)):
        # Colors, line width and bold font: 
        self.set_y(80)
        self.set_fill_color(217, 226, 243)
        self.set_text_color(0)
        self.set_draw_color(255, 255, 255)
        self.set_line_width(0.3)
        self.set_font('Arial', 'B', 7)
        for col_width, heading in zip(col_widths, headings):
            self.cell(col_width, 7, heading, 1, 0, "C", True)
        self.ln()
        # Color and font restoration:
        self.set_fill_color(217, 226, 243)
        self.set_text_color(0)
        self.set_font('Arial', '', 6)
        fill = True
        for row in rows:
            self.cell(col_widths[0], 6, row[0], "TLRB", 0, 'C', fill)
            self.cell(col_widths[1], 6, row[1], "TLRB", 0, "C", fill)
            self.cell(col_widths[2], 6, row[2], "TLRB", 0, "C", fill)
            self.cell(col_widths[3], 6, row[3], "TLRB", 0, "C", fill)
            self.cell(col_widths[4], 6, row[4], "TLRB", 0, "C", fill)
            self.cell(col_widths[5], 6, row[5], "TLRB", 0, "C", fill)
            self.cell(col_widths[6], 6, row[6], "TLRB", 0, "C", fill)
            self.cell(col_widths[7], 6, row[7], "TLRB", 0, "C", fill)
            self.cell(col_widths[8], 6, row[8], "TLRB", 0, "C", fill)
            self.ln()
            # fill = not fill
        self.cell(sum(col_widths), 0, "", "T")
        self.ln()
        self.set_fill_color(217, 226, 243)
        self.cell(col_widths[0], 6, "TOTAL "+totales[0], "TLRB",0, "C", fill)
        self.cell(col_widths[1], 6, totales[1], "TLRB",0, "C", fill)
        self.cell(col_widths[2]+col_widths[3]+col_widths[4]+col_widths[5], 6, "", "TLRB",0, "C",fill)
        self.cell(col_widths[5], 6, totales[2]+" m3", "TLRB",0, "C", fill)
        self.cell(col_widths[6], 6, totales[3]+" mt", "TLRB",0, "C", fill)
        self.cell(col_widths[7], 6, totales[4]+" mt", "TLRB",0, "C", fill)

    def tablaCita(self, headings, rows, col_widths=(30, 20, 30, 85, 20)):
        # Colors, line width and bold font: 
        self.set_y(80)
        self.set_fill_color(217, 226, 243)
        self.set_text_color(0)
        self.set_draw_color(255, 255, 255)
        self.set_line_width(0.3)
        self.set_font('Arial', 'B', 8)
        for col_width, heading in zip(col_widths, headings):
            self.cell(col_width, 7, heading, 1, 0, "C", True)
        self.ln()
        # Color and font restoration:
        self.set_fill_color(217, 226, 243)
        self.set_text_color(0)
        self.set_font('Arial', '', 6)
        fill = True
        for row in rows:
            self.cell(col_widths[0], 6, row[0], "TLRB", 0, 'C', fill)
            self.cell(col_widths[1], 6, row[1], "TLRB", 0, "C", fill)
            self.cell(col_widths[2], 6, row[2], "TLRB", 0, "C", fill)
            self.cell(col_widths[3], 6, row[3], "TLRB", 0, "C", fill)
            self.cell(col_widths[4], 6, row[4], "TLRB", 0, "C", fill)
            self.ln()
            # fill = not fill
        self.cell(sum(col_widths), 0, "", "T")
