from PIL import Image,ImageFile
from time import sleep
from .console_controls import ConsoleOutputControls
from .canvas_elements import AbstractCanvasElement,BrailleChar,Rectangle
from .canvas import Canvas
def add_open_image(c:Canvas,img:ImageFile,x:int=0,y:int=0,w:int|None=None,h:int|None=None,skipcolor:tuple[int,int,int] | None = None):
    if w is None:
        w = c.w-x
    if h is None:
        h = c.h-y
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.thumbnail((w,h))
    w, h = img.size
    matrix = img.load()
    for xi in range(w):
        for yi in range(h):
            cl = matrix[xi,yi]
            if cl==skipcolor: continue
            c.draw_point(xi+x,yi+y,cl)
def add_image(c:Canvas,path:str,x:int=0,y:int=0,w:int|None=None,h:int|None=None,skipcolor:tuple[int,int,int] | None = None):
    add_open_image(c,Image.open(path),x,y,w,h,skipcolor)
class AnimatedImage:
    def __init__(self, path, w: int|None=None, h: int|None=None,
                default_element_type: type[AbstractCanvasElement]=BrailleChar):
        self.path = path
        self.canvas = Canvas(w, h, default_element_type)
        self.w = w
        self.h = h
        self.element_type = default_element_type

    def extract_frames(self):
        """Yield each frame as a separate Image object"""
        with Image.open(self.path) as img:
            for frame in range(img.n_frames):
                img.seek(frame)
                frame_img = img.copy()
                yield frame_img

    def view_frames(self):
        for i, frame in enumerate(self.extract_frames()):
            self.canvas = Canvas(self.w, self.h, self.element_type)
            add_open_image(self.canvas, frame)
            yield self.canvas,frame.info.get("duration",100)

    def animate(self,times:int=-1,preload:bool=False):
        if times==0: return
        frames = list(self.view_frames()) if preload else []
        cache=times!=1
        try:
            if not preload:
                times-=1
                for (frame_canvas,t) in self.view_frames():
                    if cache: frames.append((frame_canvas,t))
                    with ConsoleOutputControls.keep_position():
                        print(frame_canvas,end="")
                        sleep(t/1000)
            while times>0:
                for (frame_canvas,t) in frames:
                    with ConsoleOutputControls.keep_position():
                        print(frame_canvas,end="")
                        sleep(t/1000)
                times-=1
        except KeyboardInterrupt:
            print("\nAnimation stopped")


def animation_demo(times:int=-1,preload:bool=False):
    anim = AnimatedImage("little-cute.gif", 150, 200, Rectangle)
    anim.animate(times,preload)
    ConsoleOutputControls.clear_terminal()
if __name__ == "__main__":
    animation_demo()