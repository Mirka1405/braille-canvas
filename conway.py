from time import sleep
import braille

def count_adjacent(x:int,y:int,grid:braille.Canvas):
    n = 0
    for ix in range(-1,2):
        for iy in range(-1,2):
            if x+ix == grid.w or y+iy == grid.h: continue
            if ix==iy==0: continue
            if grid.is_pixel_on(x+ix,y+iy):
                n+=1
    return n
def tick(x:int,y:int,on:bool,grid:braille.Canvas,sec_grid:braille.Canvas):
    n = count_adjacent(x,y,grid)
    if on and (n<2 or n>3): sec_grid.set_pixel_on(x,y,False)
    elif not on and n==3: sec_grid.set_pixel_on(x,y)
    else: sec_grid.set_pixel_on(x,y,grid.is_pixel_on(x,y))

def main(g:braille.Canvas|None=None,slp:float=0.2):
    """g: initial grid, slp:float=0.2 is sleep time between frames"""
    grid,sec_grid = None,None
    if g:
        grid=g
        sec_grid=braille.Canvas(g.w,g.h,g.element_type)
    else:
        grid=braille.Canvas(100,100)
        sec_grid=braille.Canvas(100,100)
        grid.draw_box(0,0,2,2,(255,255,255))
        grid.draw_line(0,0,0,1,(0,0,0),False)
        grid.draw_point(2,0,(0,0,0),False)
    braille.ConsoleOutputControls.save_position()
    while True:
        for y in range(grid.h):
            for x in range(grid.w):
                on = grid.is_pixel_on(x,y)
                if on or count_adjacent(x,y,grid):
                    tick(x,y,on,grid,sec_grid)

        braille.ConsoleOutputControls.load_position()
        print(grid)
        sleep(slp)
        grid,sec_grid = sec_grid,grid
if __name__ == "__main__":
    main()