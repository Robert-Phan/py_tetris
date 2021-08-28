import curses
from dataclasses import dataclass
from math import cos, sin
import time
from typing import Callable

forbidden = set()

@dataclass
class Tetris:
    '''Class for a tetris piece'''
    coords: list[tuple]
    pivot_point: int #pivot
    screen: curses.window
    color: int
    
    # * these methods take self.coords and return and new set of coords
    def fall(self):
        new_coords = [(x,y+1) for (x,y) in self.coords]
        if forbidden & set(new_coords):
            return self.coords
        self.pivot_point = self.pivot_point[0], self.pivot_point[1]+1
        return new_coords
        
    def move_left(self):
        new_coords = [(x-1,y) for (x,y) in self.coords]
        if forbidden & set(new_coords):
            return self.coords
        self.pivot_point = self.pivot_point[0]-1, self.pivot_point[1]
        return new_coords
    
    def move_right(self):
        new_coords =  [(x+1,y) for (x,y) in self.coords]
        if forbidden & set(new_coords):
            return self.coords
        self.pivot_point = self.pivot_point[0]+1, self.pivot_point[1]
        return new_coords

    def turn(self, direction):
        radians = 1.57079632679 if direction == "left" else -1.57079632679
        cos_theta = cos(radians) #for calculations
        sin_theta = sin(radians)
        
        (pivot_x, pivot_y) = self.pivot_point
        
        new_coords = []
        for (x,y) in self.coords:
            # I found these calculations online
            new_x = cos_theta * (x - pivot_x) - sin_theta * (y - pivot_y) + pivot_x
            new_y = sin_theta * (x - pivot_x) + cos_theta * (y - pivot_y) + pivot_y
            new_coords.append((round(new_x), round(new_y)))
        return self.coords if forbidden & set(new_coords) else new_coords
    
    def update(self, update_func: Callable[[], list]):
        new_coords = update_func() 
        if sorted(new_coords) == sorted(self.coords): 
            return 1
        # * deletes previous block
        for x, y in self.coords:
            self.screen.addstr(y, x*2, "  ")
        # * add in new coords
        for x, y in new_coords:
            self.screen.addstr(y, x*2, "  ", curses.color_pair(self.color))
            
        self.coords = new_coords

