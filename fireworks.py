import braille
from time import sleep
from random import choice, random
from math import floor

class Firework:
    def __init__(self,c:braille.Canvas,x:int,length:int=3,color:braille.ColorType=(255,0,0),explosion_chance:float=0.015):
        self.c = c
        self.x,self.y = x,c.h
        self.removable = False
        self.color = color
        self.__l = length
        self.__particles:list[Particle] = []
        self.__ec=explosion_chance
        self.__moving = True
    def tick(self):
        for i in self.__particles: i.tick()
        if not self.__particles and not self.__moving:
            self.removable=True
            return
        if self.__particles: return
        self.c.draw_line(self.x,self.y,self.x,self.y+self.__l,self.color)
        self.y-=1
        if random()<self.__ec:
            self.__particles=[Particle(self.c,self.x,self.y,color=self.color) for _ in range(10)]
            self.__moving = False
class Particle:
    def __init__(self,c:braille.Canvas,x:int,y:int,length:int=3,color:braille.ColorType=(255,0,0),burnout_chance:float=0.03):
        self.vx,self.vy=random()*8-4,random()*-3
        self.__trail:list[tuple[int,int]] = []
        self.color = color
        self.x,self.y = x,y
        self.__l = length
        self.c = c
        self.removable = False
        self.__bc = burnout_chance
        self.__moving = True
    def tick(self):
        for i in self.__trail:self.c.draw_point(*i,color=self.color)
        if len(self.__trail)>self.__l:self.__trail.pop(0)
        if not self.__moving:
            if not self.__trail:self.removable=True
            else: self.__trail.pop(0)
            return
        self.x+=self.vx
        self.y+=self.vy
        self.vx*=0.8
        if self.vy<0.3:self.vy+=0.1
        self.c.draw_point(int(self.x),int(self.y),self.color)
        self.__trail.append((int(self.x),int(self.y)))
        if random()<self.__bc:self.__moving=False

def main():
    text = "(кста это поздравление написано на питоне)"
    text2= "С др, Юрчик!"
    c = braille.Canvas(200,100)
    rainbow = braille.RainbowGradient()
    fire = braille.GradientColor((255,255,0),(255,0,0),(100,50),50)
    colors = [(255,0,0),(0,255,0),(0,0,255),(0,255,255),(255,0,255),rainbow,fire]
    fireworks: list[Firework] = [Firework(c,floor(random()*c.w),color=choice(colors))]
    words = braille.Canvas(len(text)*2,4)
    while True:
        rainbow.shift()
        words.write_text(0,0,text,rainbow)
        i=0
        if random()<0.2: fireworks.append(Firework(c,floor(random()*c.w),color=choice(colors)))
        c.erase()
        while i<len(fireworks):
            fw=fireworks[i]
            fw.tick()
            if fw.removable: fireworks.pop(i)
            else: i+=1
        c.draw_border((255,255,255))
        c.write_text((c.w-len(text2)-1)//2,c.h//2,text2,fire)
        with braille.ConsoleOutputControls.keep_position():
            print(c)
            print(words)
        sleep(0.02)

if __name__=="__main__": main()