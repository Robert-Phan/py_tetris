"""Contains the class for the tetris piece."""
from __future__ import annotations
import curses
from dataclasses import dataclass
from math import cos, sin
from typing import Callable, NewType


forbidden = set() # blocks on the surface, the sides, the floor, etc.
Coordinates = NewType("Coordinates", list[tuple])
@dataclass
class Tetris:
    '''
    # Dataclass for Tetris piece
    ## Arguments/fields
    - `coords` - list of x-y coordinates
    - `pivot_point` - x-y for points
    - `screen` - the screen used for update
    - `color` - color of piece.
    
    ## Methods
    ### "Movement methods"
    These methods take `self.coords` and return a new list of coords, 
    representing a change in postion.
    They return `0` when the movement is invalid.
    They include:
    - `fall`
    - `shift`
    - `turn`
    
    ### `update`
    `update` takes in a movement method and paints the new coords on screen.
    When the result of the function is `False` (indicating the movement was invalid), 
    it does nothing and returns `True`.
    '''
    coords: Coordinates
    pivot_point: int #pivot
    screen: curses.window
    color: int
    
    # * these methods take self.coords and return and new set of coords
    def fall(self) -> Coordinates:
        """Movement method representing a downward movement."""
        new_coords = [(x,y+1) for (x,y) in self.coords]
        if forbidden & set(new_coords):
            return False
        self.pivot_point = self.pivot_point[0], self.pivot_point[1]+1
        return new_coords
    
    def shift(self, direction: str) -> Coordinates:
        """Movement method representing a sideways movement.
        Direction is determined using the `direction` argument."""
        sh = 1 if direction == "right" else -1
        new_coords =  [(x+sh,y) for (x,y) in self.coords]
        if forbidden & set(new_coords):
            return False
        self.pivot_point = self.pivot_point[0]+sh, self.pivot_point[1]
        return new_coords

    def turn(self, direction: str) -> Coordinates:
        """Movement method representing a turn. Direction of turn
        depends on the value of `direction`."""
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
        return False if forbidden & set(new_coords) else new_coords
    
    def update(self, update_func: Callable[[], Coordinates]):
        """
        Takes a function that produces new coordinates. 
        Deletes the old coordinates, and paints new ones.
        """
        new_coords = update_func() 
        
        if not new_coords: 
            return True
        # * deletes previous block
        for x, y in self.coords:
            self.screen.addstr(y, x*2, "  ")
        # * add in new coords
        for x, y in new_coords:
            self.screen.addstr(y, x*2, "  ", curses.color_pair(self.color))
            
        self.coords = new_coords

