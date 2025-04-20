import math
import sys
import io
class AbstractColor:
    def __init__(self): pass
    def get(self,x:int=0,y:int=0) -> tuple[int,int,int]: pass
class Color(AbstractColor):
    def __init__(self,col:tuple[int,int,int]): self.col = col
    def get(self,x=0,y=0): return self.col
class GradientColor(AbstractColor):
    def __init__(self,col1:AbstractColor,col2:AbstractColor,colcentre:tuple[int,int],maxdist:int):
        self.col1 = col1
        self.col2 = col2
        self.colcentre = colcentre
        self.maxdist = maxdist
    def get(self,x=0,y=0):
        dist = ((x-self.colcentre[0])**2+(y-self.colcentre[1])**2)**0.5 / self.maxdist
        if dist>1: dist = 1
        r1,g1,b1 = self.col1.get(x,y)
        r2,g2,b2 = self.col2.get(x,y)
        return int(r2*dist+r1*(1-dist)),int(g2*dist+g1*(1-dist)),int(b2*dist+b1*(1-dist))
ColorType=AbstractColor|tuple[int,int,int]|None

class BrailleChar:
    def __init__(self):
        self.data = 0
        self.col: tuple[int,int,int] | None = None #"\e[0m"
    def set_bit(self,x:int,y:int,bit=True):
        if self.get_bit(x,y)!=bit:
            self.flip_bit(x,y)
    def flip_bit(self,x:int,y:int):
        if y<3:
            self.data^=1<<(y+x*3)
            return
        self.data^=64<<x
    def get_bit(self,x:int,y:int) -> bool:
        if y<3:
            return bool(self.data&(1<<(y+x*3)))
        return bool(self.data&(64<<x))
    def __str__(self): return chr(10240+self.data)
    def set_color(self,r:int,g:int,b:int): self.col = r,g,b
    def reset_color(self): self.col=None
    def get_color_str(self):
        return "\033[0m" if self.col is None else f"\033[38;2;{self.col[0]};{self.col[1]};{self.col[2]}m"
    def add_color_weighted(self,other:tuple[int,int,int]|None,weight:int=1):
        if self.col is None: self.col = (255,255,255)
        if other is None: other = (255,255,255)
        bc = self.data.bit_count()
        own_weight = bc-weight
        r,g,b=self.col[0]*own_weight+other[0]*weight,\
              self.col[1]*own_weight+other[1]*weight,\
              self.col[2]*own_weight+other[2]*weight
        self.col = r//bc,g//bc,b//bc
class Canvas:
    @staticmethod
    def set_stdout_to_UTF8():
        if sys.stdout.encoding!="utf-8":
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    def __init__(self,w:int,h:int):
        self.w,self.h = w,h
        self.data: list[list[BrailleChar]] = [[BrailleChar() for _ in range(math.ceil(h/4))] for _ in range(math.ceil(w/2))]
    def erase(self):
        self.data: list[list[BrailleChar]] = [[BrailleChar() for _ in range(math.ceil(self.h/4))] for _ in range(math.ceil(self.w/2))]
    def draw_point(self,x:int,y:int,color:ColorType = None,on=True):
        if self.w<=x or self.h<=y or x < 0 or y < 0: return 
        c=self.data[x//2][y//4]
        c.set_bit(x%2,y%4,on)
        c.add_color_weighted((color.get(x,y) if isinstance(color,AbstractColor) else color) if color else None)
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
        if filled:
            for i in range(y1,y2+1): self.draw_line(x1,i,x2,i,color)
            return
        self.draw_line(x1,y1,x2,y1,color)
        self.draw_line(x1,y2,x2,y2,color)
        self.draw_line(x1,y1,x1,y2,color)
        self.draw_line(x2,y1,x2,y2,color)
    def draw_border(self,color:ColorType=None,on=True): self.draw_box(0,0,self.w-1,self.h-1,color,on=on)
    def __str__(self):
        rows = []
        lastcol = None
        for y in range(len(self.data[0])):
            row = []
            for x in range(len(self.data)):
                c = self.data[x][y]
                if c.data!=0 and lastcol!=c.col:
                    lastcol=c.col
                    row.append(c.get_color_str())
                row.append(str(c))
            rows.append(''.join(row))
        return '\n'.join(rows)+"\033[0m"

if __name__ == "__main__":
    Canvas.set_stdout_to_UTF8()
    c = Canvas(64,64)
    ui = Canvas(64,4)
    grad = GradientColor(Color((255,0,0)),Color((0,255,255)),(1,1),86)
    c.draw_border()
    c.draw_line(62,62,1,1,grad)
    ui.draw_line(0,1,10,1,(255,0,0))
    ui.draw_line(15,1,25,1,(127,127,0))
    print(c)
    print(ui)
