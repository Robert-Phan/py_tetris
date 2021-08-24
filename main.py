import curses
import time
from tetris_class import Tetris


def main_loop(stdscr: curses.window):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
    stdscr.nodelay(True)
    curses.curs_set(0)
        
    i = 0
    g = Tetris([(0,0), (0,1), (0, 2), (1, 2)], 
               1,
               stdscr)
    # * loop 
    while True:
        stdscr.refresh()
        c = stdscr.getch()
        if c == 3: break # Ctrl + c == break
        # * controls
        if c == 97:  g.update(g.move_left)
        if c == 100: g.update(g.move_right)
        if c == 115: g.update(g.fall)
        if c == 261: g.update(lambda: g.turn(1.570796))  #left turn
        if c == 260: g.update(lambda: g.turn(-1.570796)) #right turn
        
        # * natural block falling
        i += 1
        if i == 55:
            g.update(g.fall)
            i = 0
        time.sleep(0.01)


def main():
    curses.wrapper(main_loop)

if __name__=='__main__':
    main()