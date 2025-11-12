from .canvas import Canvas
from .canvas_elements import BrailleChar
def str_to_canvas(s:str) -> Canvas:
    """This function assumes that all the characters are either \\n or unicode 10240 to 10496 (braille). All others are ignored."""
    s = ''.join(filter(lambda x:10240<=ord(x)<=10496 or x=="\n",s))
    sp = s.split("\n")
    c = Canvas(max(len(i) for i in sp)*2,len(sp)*4)
    for y,line in enumerate(sp):
        for x,i in enumerate(line):
            v = ord(i)
            bc = BrailleChar()
            bc.data = v-10240
            c.data[x][y]=bc
    return c