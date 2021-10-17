
from fpdf import FPDF 

class PDF(FPDF):
    def texto(self,text,x,y):
        self.set_xy(x,y)    
        self.set_font('Arial', 'I', 12)
        self.cell(100,40,text)
        
    def titles(self,title):
        self.set_xy(0.0,0.0)
        self.set_font('Arial', 'B', 16)
        self.cell(100, 40, align='C', txt=title, border=False)
        # self.ln(20)
        
        
    def linea(self):
        # self.line(10, 10, 10, 100)
        # self.set_xy(x,y)
        self.set_line_width(0.5)
        self.set_draw_color(103, 131, 179)
        self.line(25, 25, 185, 25)
        # X inicio, Y inicio, X fin, Y termino
        self.line(25, 75, 185, 75)