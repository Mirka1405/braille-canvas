from os.path import getsize
from braille import Canvas,Prefixes
from math import ceil
def file_to_canvas(fp:str,w:int) -> Canvas:
    c = Canvas(w,ceil(getsize(fp)/w*8),prefix=Prefixes.bold)
    x=y=0
    with open(fp,"rb") as f:
        ch= f.read(1)
        while ch:
            b = ord(ch)
            for _ in range(8):
                c.draw_point(x,y,on=bool(b&0b10000000))
                b,x = (b<<1)&0xff,x+1
                if x>=w: x,y=0,y+1
            ch= f.read(1)
    return c
if __name__ == "__main__":
    from sys import argv
    fp = argv[1] if len(argv)>1 else input("File path to use: ")
    w = int(argv[2]) if len(argv)>2 else int(input("Canvas width (note that only even amounts are reversible): "))
    fo = argv[3] if len(argv)>3 else "out.txt"
    with open(fo,"w",encoding="utf-8") as f: f.write(file_to_canvas(fp,w).str_without_color())