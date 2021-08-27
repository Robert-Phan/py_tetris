import curses
import time
import random
from tetris_class import Tetris

def init_color():
    def init_color_and_pair(number: int, r: int, g: int, b: int):
        curses.init_color(number, r, g, b)
        curses.init_pair(number, curses.COLOR_BLACK, number)
    init_color_and_pair(50, 1000, 647, 0)
    init_color_and_pair(51, 0, 0, 1000)
    init_color_and_pair(52, 1000, 0, 0)
    init_color_and_pair(53, 0, 1000, 0)
    init_color_and_pair(54, 1000, 1000, 0)
    init_color_and_pair(55, 0, 1000, 1000)
    init_color_and_pair(56, 600, 0, 800)

def spawn_block(screen: curses.window):
    templates = [
        ([(0,1), (1,1), (2,1), (2,0)], (1, 1), 50),     #orange L-shape
        ([(0,1), (1,1), (2,1), (0,0)], (1, 1), 51),     #blue L-shape
        ([(0,0), (1,0), (1,1), (2,1)], (1, 1), 52),     #red lightning
        ([(0,1), (1,1), (1,0), (2,0)], (1,1), 53),      #green lightning
        ([(0,0), (0,1), (1,0), (1,1)], (0.5, 0.5), 54), #cube
        ([(0,1), (1,1), (2,1), (3,1)], (1.5, 0.5), 55), #long
        ([(0,0), (1,0), (2,0), (1,1)], (1, 0), 56)      #T-shape
    ]
    shape, pivot, color = random.choice(templates)
    g = Tetris(shape, 
               pivot,
               screen, 
               color)
    # g.update(lambda: g.coords)
    return g

def main_loop(stdscr: curses.window):
    curses.curs_set(0)
    stdscr_y, stdscr_x = stdscr.getmaxyx()
    screen = curses.newpad(stdscr_y+2, stdscr_x)
    screen.nodelay(True)

    init_color() # initiates color for the tetris pieces

    block = spawn_block(screen)
    i = 0
    # * loop 
    while True:
        screen.refresh(2, 0, 0, 0, stdscr_y-1, stdscr_x-1)
        c = screen.getch()
        if c == 3: break # Ctrl + c == break
        # * controls
        if c == 97:  block.update(block.move_left)
        if c == 100: block.update(block.move_right)
        if c == 115: block.update(block.fall)
        if c == 106: block.update(lambda: block.turn("left"))  #left turn
        if c == 108: block.update(lambda: block.turn("right")) #right turn
        
        # * natural block falling
        i += 1
        if i == 55:
            block.update(block.fall)
            i = 0
        time.sleep(0.01)


def main():
    curses.wrapper(main_loop)

if __name__=='__main__':
    main()