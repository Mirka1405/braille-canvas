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
def get_grayscale(c: AbstractColor): return int(c[0]*0.2126+c[1]*0.7152+c[2]*0.0722)
class GrayscaleShader(AbstractShader):
    def __init__(self,conditions:list[ShaderCondition]|None=None):
        super().__init__(conditions)
    def apply_to_canvas_pixel(self,canvas:Canvas,x:int=0,y:int=0):
        c = canvas.get_pixel_color(x,y)
        if c==None: return
        gv = get_grayscale(c)
        canvas.draw_point(x,y,(gv,gv,gv),canvas.is_pixel_on(x,y))
class LuminosityFilter(AbstractShader):
    def __init__(self,minlum:int,invert:bool=False,conditions:list[ShaderCondition]|None=None,blacknwhite:bool=False):
        super().__init__(conditions)
        self.minlum = minlum
        self.invert = invert
        self.bw = blacknwhite
    def apply_to_canvas_pixel(self,canvas:Canvas,x:int=0,y:int=0):
        c = canvas.get_pixel_color(x,y)
        if c==None: return
        gv = get_grayscale(c)
        enable = (gv>self.minlum)!=self.invert
        col = 255 if enable else 0
        canvas.draw_point(x,y,(col,col,col) if self.bw else (gv,gv,gv),enable)
class DitheringFilter(AbstractShader):
    def __init__(self, minlum: int = 128, invert: bool = False, conditions: list[ShaderCondition] | None = None):
        super().__init__(conditions)
        self.minlum = minlum
        self.invert = invert
    
    def apply_to_canvas(self, canvas: Canvas, x: int = 0, y: int = 0, w: int | None = None, h: int | None = None, *args, **kwargs):
        if w is None: w = canvas.w
        elif x + w > canvas.w: w = canvas.w - x
        if h is None: h = canvas.h
        elif y + h > canvas.h: h = canvas.h - y
        
        grayscale = []
        for iy in range(h):
            row = []
            for ix in range(w):
                if not self.conditions or self.check_conditions(canvas, x + ix, y + iy):
                    c = canvas.get_pixel_color(x + ix, y + iy)
                    if c is None:
                        row.append(0)
                    else:
                        row.append(get_grayscale(c))
                else:
                    row.append(0)
            grayscale.append(row)
        
        for iy in range(h):
            for ix in range(w):
                if self.conditions and not self.check_conditions(canvas, x + ix, y + iy):
                    continue
                    
                old_pixel = grayscale[iy][ix]
                new_pixel = 255 if old_pixel > self.minlum else 0
                if self.invert:
                    new_pixel = 255 - new_pixel
                canvas.draw_point(x + ix, y + iy, (new_pixel, new_pixel, new_pixel), new_pixel > 0)
                quant_error = old_pixel - new_pixel
                
                if ix + 1 < w:
                    grayscale[iy][ix + 1] = min(255, max(0, grayscale[iy][ix + 1] + quant_error * 7/16))
                if ix - 1 >= 0 and iy + 1 < h:
                    grayscale[iy + 1][ix - 1] = min(255, max(0, grayscale[iy + 1][ix - 1] + quant_error * 3/16))
                if iy + 1 < h:
                    grayscale[iy + 1][ix] = min(255, max(0, grayscale[iy + 1][ix] + quant_error * 5/16))
                if ix + 1 < w and iy + 1 < h:
                    grayscale[iy + 1][ix + 1] = min(255, max(0, grayscale[iy + 1][ix + 1] + quant_error * 1/16))
    
    def apply_to_canvas_pixel(self, canvas: Canvas, x: int = 0, y: int = 0, *args, **kwargs):
        raise NotImplementedError("DitheringFilter requires processing the entire canvas at once")
class AdaptiveThresholdFilter(AbstractShader):
    def __init__(self, block_size: int = 11, c: int = 2, invert: bool = False, conditions: list[ShaderCondition] | None = None):
        super().__init__(conditions)
        self.block_size = block_size
        self.c = c
        self.invert = invert
    
    def apply_to_canvas(self, canvas: Canvas, x: int = 0, y: int = 0, w: int | None = None, h: int | None = None, *args, **kwargs):
        if w is None: w = canvas.w
        elif x + w > canvas.w: w = canvas.w - x
        if h is None: h = canvas.h
        elif y + h > canvas.h: h = canvas.h - y
        
        block_size = max(3, self.block_size | 1)
        half_block = block_size // 2

        grayscale = []
        for iy in range(h):
            row = []
            for ix in range(w):
                if not self.conditions or self.check_conditions(canvas, x + ix, y + iy):
                    c = canvas.get_pixel_color(x + ix, y + iy)
                    if c is None:
                        row.append(0)
                    else:
                        row.append(get_grayscale(c))
                else:
                    row.append(0)
            grayscale.append(row)
        
        for iy in range(h):
            for ix in range(w):
                if self.conditions and not self.check_conditions(canvas, x + ix, y + iy):
                    continue
                
                current_val = grayscale[iy][ix]
                
                sum_val = 0
                count = 0
                
                for dy in range(-half_block, half_block + 1):
                    for dx in range(-half_block, half_block + 1):
                        ny, nx = iy + dy, ix + dx
                        if 0 <= ny < h and 0 <= nx < w:
                            sum_val += grayscale[ny][nx]
                            count += 1
                
                if count > 0:
                    local_mean = sum_val / count
                    threshold = local_mean - self.c
                    
                    new_pixel = 255 if current_val >= threshold else 0
                    if self.invert:
                        new_pixel = 255 - new_pixel
                    
                    canvas.draw_point(x + ix, y + iy, (current_val, current_val, current_val), new_pixel > 0)
    
    def apply_to_canvas_pixel(self, canvas: Canvas, x: int = 0, y: int = 0, *args, **kwargs):
        raise NotImplementedError("AdaptiveThresholdFilter requires processing the entire canvas at once")