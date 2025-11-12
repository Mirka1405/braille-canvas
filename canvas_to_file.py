from braille import Canvas
from braille.str_to_canvas import str_to_canvas
def canvas_to_file(c:Canvas,remove_trailing_nul=True) -> bytes:
    b = [0]
    t = 0
    for y in range(c.h):
        for x in range(c.w):
            b[-1]=(b[-1]<<1)|c.is_pixel_on(x,y)
            t+=1
            if t>=8:
                b.append(0)
                t=0
    if remove_trailing_nul:
        while b[-1]==0:b.pop()
    return bytes(b)
            
if __name__ == "__main__":
    from sys import argv
    fp = argv[1] if len(argv)>1 else input("File path to use: ")
    fo = argv[2] if len(argv)>2 else "out.txt"
    rtn = bool(int(argv[3])) if len(argv)>3 else True
    c = None
    with open(fp,"r",encoding="utf-8") as f: c = str_to_canvas(f.read())
    with open(fo,"wb") as f: f.write(canvas_to_file(c,rtn))