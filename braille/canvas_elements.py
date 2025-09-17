from .colors import BasicColorType
class AbstractCanvasElement:
    def __init__(self,color:tuple[int,int,int]|None=None):
        self.colors: list[BasicColorType] = [color for _ in range(8)]

    @property
    def color(self):
        r,g,b,n = 0,0,0,0
        for i in self.colors:
            if i is not None:
                r,g,b=r+i[0],g+i[1],b+i[2]
                n+=1
        if n==0: return None
        return r//8,g//8,b//8
    def is_empty(self) -> bool: return True
    def set_bit(self,x:int,y:int,bit=True): pass
    def __str__(self): pass
    def reset_colors(self): self.colors = [None for _ in range(8)]
    def set_pixel_color(self,x:int,y:int,color:BasicColorType):
        self.colors[x*4+y]=color
    def get_pixel_color(self,x:int,y:int) -> BasicColorType:
        return self.colors[x*4+y]
    def get_color_str(self):
        return "\033[0m" if self.color is None else f"\033[38;2;{self.color[0]};{self.color[1]};{self.color[2]}m"
    def get_bit(self,x:int,y:int) -> bool: return False
class BrailleChar(AbstractCanvasElement):
    def __init__(self,color:tuple[int,int,int]|None=None):
        super().__init__(color)
        self.data = 0
    @property
    def color(self):
        r,g,b = 0,0,0
        n=0
        for x in range(2):
            for y in range(4):
                c=self.get_pixel_color(x,y)
                if c is not None and self.get_bit(x,y):
                    r,g,b=r+c[0],g+c[1],b+c[2]
                    n+=1
        if n==0: return None
        return r//n,g//n,b//n
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
    def is_empty(self): return self.data==0
class SimpleChar(AbstractCanvasElement):
    def __init__(self,char:str,color:tuple[int,int,int]|None=None):
        super().__init__(color)
        self.c = char
    def __str__(self): return self.c
    def is_empty(self): return self.c.isspace()
class Rectangle(AbstractCanvasElement):
    def __init__(self, color = None):
        super().__init__(color)
    def __str__(self): return " "
    def get_color_str(self):
        return "\033[0m" if self.color is None else f"\033[48;2;{self.color[0]};{self.color[1]};{self.color[2]}m"
    def is_empty(self): return self.color is None
