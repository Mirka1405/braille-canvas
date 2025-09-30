from random import randint, random
from braille import Canvas,ConsoleOutputControls
from time import sleep
class Heart:
    def __init__(self,canvas:Canvas,x:int,y:int):self.c,self.x,self.y=canvas,x,y
    def move_down(self):
        self.c.draw_point(self.x,self.y+1,None,False)
        self.c.draw_point(self.x+1,self.y,None,False)
        self.c.draw_point(self.x+2,self.y+1,None,False)
        self.c.draw_point(self.x+3,self.y,None,False)
        self.c.draw_point(self.x+4,self.y+1,None,False)
        self.c.draw_point(self.x,self.y+3,(255,0,0))
        self.c.draw_point(self.x+1,self.y+4,(255,0,0))
        self.c.draw_point(self.x+2,self.y+5,(255,0,0))
        self.c.draw_point(self.x+3,self.y+4,(255,0,0))
        self.c.draw_point(self.x+4,self.y+3,(255,0,0))
        self.y+=1
    @classmethod
    def random(cls,c:Canvas):return cls(c,randint(1,c.w-5),-5)
if __name__ == "__main__":
    hearts: list[Heart] = []
    c = Canvas(200,80)
    hearts.append(Heart.random(c))
    while True:
        sleep(0.1)
        if random()<0.3: hearts.append(Heart.random(c))
        i=0
        while i<len(hearts):
            h=hearts[i]
            h.move_down()
            if h.y>=c.h:hearts.pop(i)
            else:i+=1
        c.write_text(c.w//2,c.h//2-1,"I love you,\n  ????!",(255,127,127))
        with ConsoleOutputControls.keep_position():print(c)