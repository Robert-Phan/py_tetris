import curses
import time
import random
from tetris_class import Tetris, forbidden


class Game:
    
    height, width = 34, 40
    fallen_blocks = set()
    fail_line = 7

    @staticmethod
    def main(stdscr: curses.window):
        Game.screen = curses.newpad(Game.height+2, Game.width)
        curses.curs_set(0)
        curses.resize_term(Game.height, Game.width*2)
        Game.screen.nodelay(True)
        Game.screen.border()
        
        Game.border = {(x, Game.height+1) for x in range(Game.width)} | \
        {(0, y) for y in range(Game.height+2)} | {(Game.width // 2-1, y) for y in range(Game.height+2)}
        forbidden.update(Game.border)
        
        Game.init_color()
        
        block = Game.spawn_block()
        i = 0
        # * loop 
        while True:
            Game.screen.refresh(2, 0, 0, 0, Game.height-1, Game.width-1)
            c = Game.screen.getch()
            if c == 3: break # Ctrl + c == break
            # * controls
            if c == 115: 
                g = Game.fall(block)
                if g: block = g

            if c == 97:  block.shift("left")
            if c == 100: block.shift("right")
            if c == 106: block.turn("left") 
            if c == 108: block.turn("right") 

            # * natural block falling
            i += 1
            if i == 55: 
                g = Game.fall(block)
                if g: block = g
                i = 0

            Game.remove_line()   
            Game.check_for_fail()
            time.sleep(0.01)
        

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
    
    def spawn_block():
        """Selects a random template for a block, returns new block."""
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
        t = random.randint(0, Game.width // 2 - 4)
        g = Tetris([(x+t, y) for (x, y) in shape], 
                   (pivot[0]+t, pivot[1]),
                   Game.screen, 
                   color)
        return g
    
    def fall(block: Tetris):
        """
        Function for falling block.
        
        `block.fall` is decorated, so by default will return `None`. In that case, it returns False.
        
        In the case that `block.fall` returns True, representing it hit another block/the floor,
        the block's coords will be added to `forbidden`, and a new block will be made.
        """
        if not block.fall(): return False
        
        forbidden.update(set(block.coords))
        Game.fallen_blocks.update({(y, x, block.color) for (x, y) in block.coords})
        
        new_block = Game.spawn_block()
        new_block.fall()
        return new_block
    
    @staticmethod
    def tuples_to_dict(tu: set[tuple]):
        di = {}
        for a, b in tu:
            di.setdefault(a, []).append(b)
        return di

    def check_for_line():
        """Returns the first full line from bottoms up when detected."""
        g = Game.tuples_to_dict({(y, (x, c)) for (y, x, c) in Game.fallen_blocks}).items()
        g = list(g)
        g.sort(reverse=True)
        
        for y, x_c in g:
            xs = {x for (x, c) in x_c}
            if sorted(xs) == list(range(1, Game.width // 2 - 1)): return y
    
    def remove_line():
        """Removes detected line from `check_for_line`."""
        new_fallen_blocks, new_forbidden = set(), set()
        change_levi = []
        _y = Game.check_for_line()
        if _y:
            for y, x, c in Game.fallen_blocks:
                if y < _y:
                    change_levi.append((y, x, c))
                elif y != _y:
                    new_fallen_blocks.add((y, x, c))
                    new_forbidden.add((x, y))
                else:
                    Game.screen.addstr(y, x*2, "  ")
            # make all the blocks above a remove line fall down
            change_levi.sort(reverse=True)
            for y, x, c in change_levi:
                if y > 1:
                    Game.screen.addstr(y, x*2, "  ")
                    Game.screen.addstr(y+1, x*2, "  ", curses.color_pair(c))
                    new_fallen_blocks.add((y+1, x, c))
                    new_forbidden.add((x, y+1))
            
            Game.fallen_blocks.clear(); Game.fallen_blocks.update(new_fallen_blocks)
            forbidden.clear(); forbidden.update(new_forbidden | Game.border)

    def check_for_fail():
        g = any({y == Game.fail_line for (y, *_) in Game.fallen_blocks})
        if g:
            raise Exception
        
        
if __name__ == "__main__":
    curses.wrapper(Game.main)