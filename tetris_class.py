import curses
from dataclasses import dataclass
from typing import Callable

@dataclass
class Tetris:
    '''Class for a tetris piece'''
    coords: list[tuple]
    rel_coords: list[list[tuple]]
    screen: curses.window
    
    @staticmethod
    # * Converts coordinates into x-as-key dicts
    def convert(tup: list[tuple]) -> list[tuple]:
        di = dict()
        for (a, b) in tup:
            di.setdefault(a, []).append(b)
        return list(di.items())
    # * these methods take self.coords and return and new set of coords
    def fall(self):
        return [(x,y+1) for (x,y) in self.coords]
        
    def move_left(self):
        return [(x-1,y) for (x,y) in self.coords]
    
    def move_right(self):
        return [(x+1,y) for (x,y) in self.coords]
    
    def update(self, update_func: Callable[[], list]):
        # * deletes previous block
        for i, (x, ys) in enumerate(convert(self.coords)):
            for y in ys:
                self.screen.addstr(y, x + i, " ")
                self.screen.addstr(y, x + i + 1, " ")

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
        new_coords = update_func() 
        for i, (x, ys) in enumerate(convert(new_coords)):
            for y in ys:
                self.screen.addstr(y, x + i, " ", curses.color_pair(1))
                self.screen.addstr(y, x + i + 1, " ", curses.color_pair(1))
            
        self.coords = new_coords

def convert(tup: list[tuple]) -> list[tuple]:
    di = dict()
    for (a, b) in tup:
        di.setdefault(a, []).append(b)
    return list(di.items())

