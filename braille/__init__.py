from .canvas import *
from .canvas_elements import *
from .colors import *
from .shaders import *
from .console_controls import *
from .images import *
__all__ = ["shaders","canvas","colors","images","console_controls","canvas_elements"]
import sys
from io import TextIOWrapper
def set_stdout_to_UTF8():
    if sys.stdout.encoding!="utf-8":
        sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
def demo():
    c = Canvas(64,64)
    ui = Canvas(64,4)
    grad = GradientColor(SolidColor((255,0,0)),SolidColor((0,0,255)),(1,1),87)
    textgrad = RainbowGradient(30)
    bordergrad = RainbowGradient(140)
    c.draw_border(bordergrad)
    c.draw_box(59,59,4,4,grad,filled=True)
    ui.draw_line(0,1,10,1,(255,0,0))
    ui.draw_line(15,1,25,1,(127,127,0))
    c.write_text(c.w//2-3,c.h//2-1,"Hello\nWorld!",textgrad)
    print(c)
    print(ui)
if __name__ == "__main__":
    demo()
