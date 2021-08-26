import curses
import time
import random
from tetris_class import Tetris

def spawn_block(screen: curses.window):
    templates = [
        ([(0,1), (1,1), (2,1), (2,0)], (1, 1)),     #orange L-shape
        ([(0,1), (1,1), (2,1), (0,0)], (1, 1)),     #blue L-shape
        ([(0,0), (1,0), (1,1), (2,1)], (1, 1)),     #red lightning
        ([(0,1), (1,1), (1,0), (2,0)], (1,1)),      #green lightning
        ([(0,0), (0,1), (1,0), (1,1)], (0.5, 0.5)), #cube
        ([(0,1), (1,1), (2,1), (3,1)], (1.5, 0.5)), #long
        ([(0,0), (1,0), (2,0), (1,1)], (1, 0))      #T-shape
        
    ]
    block_temp = random.choice(templates)
    g = Tetris(block_temp[0], 
               block_temp[1],
               screen)
    # g.update(lambda: g.coords)
    return g

def main_loop(stdscr: curses.window):
    curses.curs_set(0)
    stdscr_y, stdscr_x = stdscr.getmaxyx()
    screen = curses.newpad(stdscr_y+2, stdscr_x)
    screen.nodelay(True)
    curses.init_pair(100, curses.COLOR_BLUE, curses.COLOR_WHITE)
    screen.bkgd(" ", curses.color_pair(100))
        
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