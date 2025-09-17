class AbstractColor:
    def __init__(self): pass
    def get(self,x:int=0,y:int=0) -> tuple[int,int,int]: return 0,0,0
class SolidColor(AbstractColor):
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
class RainbowGradient(AbstractColor):
    def __init__(self, period:int=100, shift:int = 0):
        self.period = period
        self.shift_amount = shift
    def shift(self,amount:int=1):
        self.shift_amount += amount
    def get(self, x=0, y=0):
        diag = x + y + self.shift_amount
        t = (diag % self.period) / self.period
        hue = t * 360
        return self.hue_to_rgb(hue)
    def hue_to_rgb(self, hue):
        hue = hue % 360
        h = hue / 60.0
        c = 255
        x = int(c * (1 - abs((h % 2) - 1)))
        
        if h < 1:
            return (c, x, 0)
        elif h < 2:
            return (x, c, 0)
        elif h < 3:
            return (0, c, x)
        elif h < 4:
            return (0, x, c)
        elif h < 5:
            return (x, 0, c)
        else:
            return (c, 0, x)
BasicColorType=tuple[int,int,int]|None
ColorType=AbstractColor|BasicColorType
def to_base_color(color:ColorType,x:int=0,y:int=0) -> BasicColorType:
    return color.get(x,y) if isinstance(color,AbstractColor) else color
