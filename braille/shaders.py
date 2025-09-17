from .canvas import Canvas
from .colors import AbstractColor,RainbowGradient
class ShaderCondition:
    def check(self,canvas:Canvas,x:int=0,y:int=0) -> bool: return True
class NonEmptyShaderCondition:
    def check(self,canvas:Canvas,x:int=0,y:int=0) -> bool:
        return canvas.get_pixel_color(x,y) is not None
class WhitePixelsShaderCondition:
    def check(self,canvas:Canvas,x:int=0,y:int=0) -> bool:
        return canvas.get_pixel_color(x,y) == (255,255,255)
class AbstractShader:
    def __init__(self,conditions:list[ShaderCondition]|None=None):
        self.conditions = conditions
    def apply_to_canvas(self,canvas:Canvas,x:int=0,y:int=0,w:int|None=None,h:int|None=None,*args, **kwargs):
        if w is None: w = canvas.w
        elif x+w>canvas.w: w = canvas.w-x
        if h is None: h = canvas.h
        elif y+h>canvas.h: h = canvas.h-y
        for ix in range(w):
            for iy in range(h):
                self.apply_to_canvas_pixel(canvas,x+ix,y+iy,*args,**kwargs)
    def apply_to_canvas_pixel(self,canvas:Canvas,x:int=0,y:int=0,*args, **kwargs):
        pass
    def check_conditions(self,canvas:Canvas,x:int=0,y:int=0):
        for i in self.conditions:
            if not i.check(canvas,x,y): return False
        return True

class SetColorShader(AbstractShader):
    def __init__(self,color: AbstractColor,conditions:list[ShaderCondition]|None=None):
        super().__init__(conditions)
        self.color = color
    def apply_to_canvas_pixel(self,canvas:Canvas,x:int=0,y:int=0):
        if not self.check_conditions(canvas,x,y): return
        canvas.draw_point(x,y,self.color)
class RainbowShader(SetColorShader):
    color:RainbowGradient
    def __init__(self,color: RainbowGradient,conditions:list[ShaderCondition]|None=None):
        super().__init__(color,conditions)
    def shift(self,n:int=1):
        self.color.shift(n)