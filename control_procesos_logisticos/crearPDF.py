
from fpdf import FPDF 

class PDF(FPDF):
    def texto(self,text,x,y):
        self.set_xy(x,y)    
        self.set_font('Arial', '', 12)
        self.cell(100,40,text)
        
    def titles(self,title):
        self.set_xy(0.0,0.0)
        self.set_font('Arial', 'B', 16)
        self.cell(100, 40, align='C', txt=title, border=False)
        # self.ln(20)
        
        
    def draw_lines(self):
        # self.line(10, 10, 10, 100)
        self.set_line_width(1)
        self.set_draw_color(255, 0, 0)
        self.line(20, 20, 100, 20)