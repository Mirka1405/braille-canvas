from .colors import ColorType,BasicColorType,to_base_color
from .canvas_elements import AbstractCanvasElement,BrailleChar,SimpleChar
import math

class Canvas:
    def __init__(self,w:int,h:int,default_element_type:type[AbstractCanvasElement]=BrailleChar):
        self.w,self.h = w,h
        self.element_type=default_element_type
        self.data: list[list[AbstractCanvasElement]] = [[self.element_type() for _ in range(math.ceil(h/4))] for _ in range(math.ceil(w/2))]
    def erase(self):
        self.data: list[list[AbstractCanvasElement]] = [[self.element_type() for _ in range(math.ceil(self.h/4))] for _ in range(math.ceil(self.w/2))]
    def draw_point(self,x:int,y:int,color:ColorType = None,on=True):
        if self.w<=x or self.h<=y or x < 0 or y < 0: return 
        c=self.data[x//2][y//4]
        c.set_bit(x%2,y%4,on)
        c.set_pixel_color(x%2,y%4,to_base_color(color,x,y))
    def set_pixel_on(self,x:int,y:int,on=True):
        c=self.data[x//2][y//4]
        c.set_bit(x%2,y%4,on)
    def get_pixel_color(self,x:int,y:int) -> BasicColorType:
        if 0>x>self.w or 0>y>self.h: return None
        return self.data[x//2][y//4].get_pixel_color(x%2,y%4)
    def is_pixel_on(self,x:int,y:int) -> bool:
        if 0>x>self.w or 0>y>self.h: return False
        return self.data[x//2][y//4].get_bit(x%2,y%4)
    def draw_line(self, x1: int, y1: int, x2: int, y2: int,color:ColorType = None,on=True):
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.draw_point(x1, y,color,on)
            return
        if y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.draw_point(x, y1,color,on)
            return
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            self.draw_point(x1, y1,color,on)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
    def draw_box(self, x1: int, y1: int, x2: int, y2: int,color:ColorType = None,filled=False,on=True):
        if x1>x2: x1,x2=x2,x1
        if y1>y2: y1,y2=y2,y1
        if filled:
            for i in range(y1,y2+1): self.draw_line(x1,i,x2,i,color)
            return
        self.draw_line(x1,y1,x2,y1,color,on)
        self.draw_line(x1,y2,x2,y2,color,on)
        self.draw_line(x1,y1,x1,y2,color,on)
        self.draw_line(x2,y1,x2,y2,color,on)
    def draw_border(self,color:ColorType=None,on=True): self.draw_box(0,0,self.w-1,self.h-1,color,on=on)
    def write_text(self,start_x:int,start_y:int,text:str,color:ColorType=None):
        start_x//=2
        start_y//=4
        for y,line in enumerate(text.split("\n")):
            for x,c in enumerate(line):
                self.data[x+start_x][y+start_y]=SimpleChar(c,to_base_color(color,(x+start_x)*2,(y+start_y)*2))
    def __str__(self):
        rows = []
        lastcol = None
        lastcolstr = None
        emptyrows = 0
        for y in range(len(self.data[0])):
            row = []
            if lastcol is not None: row.append(lastcolstr)
            empty = True
            for x in range(len(self.data)):
                c = self.data[x][y]
                if not c.is_empty():
                    empty = False
                    if lastcol!=c.color:
                        lastcol=c.color
                        lastcolstr=c.get_color_str()
                        row.append(lastcolstr)
                row.append(str(c))
            if empty: emptyrows+=1
            else: emptyrows=0
            rows.append(''.join(row))
        if emptyrows>0: return '\033[0m\n'.join(rows[:-emptyrows])+"\033[0m"
        return '\033[0m\n'.join(rows)+"\033[0m"
