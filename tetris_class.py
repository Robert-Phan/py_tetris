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

    def turn(self, radians):
        cos_theta = cos(radians) #for calculations
        sin_theta = sin(radians)
        
        (pivot_x, pivot_y) = self.coords[self.pivot_point]
        
        new_coords = []
        for (x,y) in self.coords:
            # I found these calculations online
            new_x = cos_theta * (x - pivot_x) - sin_theta * (y - pivot_y) + pivot_x
            new_y = sin_theta * (x - pivot_x) + cos_theta * (y - pivot_y) + pivot_y
            new_coords.append((round(new_x), round(new_y)))
            
        return new_coords
    
    
    def print(self):
        ...
    def update(self, update_func: Callable[[], list]):
        # * deletes previous block
        for x, ys in sorted(Tetris.convert(self.coords)):
            first_x = sorted(Tetris.convert(self.coords))[0][0]
            for y in ys:
                self.screen.addstr(y, first_x + (x-first_x)*2, "  ")

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
        new_coords = update_func() 
        # * add in new coords
        for x, ys in sorted(Tetris.convert(new_coords)):
            first_x = sorted(Tetris.convert(new_coords))[0][0]
            for y in ys:
                self.screen.addstr(y, first_x + (x-first_x)*2, "  ", curses.color_pair(1))
            
        self.coords = new_coords

g = Tetris([(10,10), (10,11), (10, 12), (11, 12)], 
               1,
               curses.initscr())


