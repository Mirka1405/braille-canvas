import braille
grid = braille.Canvas(100,100)
sec_grid = braille.Canvas(100,100)

# glider
grid.draw_box(0,0,2,2,(255,255,255))
grid.draw_line(0,0,0,1,(0,0,0),False)
grid.draw_point(2,0,(0,0,0),False)

def tick(x:int,y:int):
    n = 0
    for ix in range(-1,1):
        for iy in range(-1,1):
            if ix==iy==0: continue
            if grid.is_pixel_on(x+ix,y+iy):
                n+=1
    if n<2 or n>3:
        sec_grid.set_pixel_on(x,y,False)

while True:
    for y in range(grid.h):
        for x in range(grid.w):
            if grid.is_pixel_on(x,y):
                tick(grid,x,y)
