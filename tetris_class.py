import curses
from dataclasses import dataclass
from math import cos, sin
from typing import Callable

@dataclass
class Tetris:
    '''Class for a tetris piece'''
    coords: list[tuple]
    pivot_point: int #pivot
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

    def turn_right(self):
        cos_theta = cos(1.570796)
        sin_theta = sin(1.570796)
        
        pivot = self.coords[self.pivot_point]
        (pivot_x, pivot_y) = pivot
        
        new_coords = []
        for (x,y) in self.coords:
            new_x = cos_theta * (x - pivot_x) - sin_theta * (y - pivot_y) + pivot_x
            new_y = sin_theta * (x - pivot_x) + cos_theta * (y - pivot_y) + pivot_y
            new_coords.append((round(new_x), round(new_y)))
            
        return new_coords
    
    def print(self):
        ...
    def update(self, update_func: Callable[[], list]):
        # * deletes previous block
        for i, (x, ys) in enumerate(Tetris.convert(self.coords)):
            for y in ys:
                self.screen.addstr(y, x + i, " ")
                self.screen.addstr(y, x + i + 1, " ")

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
        new_coords = update_func() 
        for i, (x, ys) in enumerate(Tetris.convert(new_coords)):
            for y in ys:
                self.screen.addstr(y, x + i, " ", curses.color_pair(1))
                self.screen.addstr(y, x + i + 1, " ", curses.color_pair(1))
            
        self.coords = new_coords

g = Tetris([(0,0), (0,1), (0, 2), (1, 2)], 
               1,
               curses.initscr())

print(g.turn_right())
print(g.turn_right())
print(g.turn_right())