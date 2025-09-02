from pygame import Vector2 as vector
import pygame as pg
from collections import deque

class Snake:
    def __init__(
            self,
            color: tuple[int, int, int]=(75, 0, 130),
            cell_size: int=None,
            columns: int=None,
            rows: int=None
        ) -> None:

        self.color = color
        self.cell_size = cell_size
        self.columns = columns
        self.rows = rows
        self.body = [
            vector(self.columns // 2, self.rows // 2),
            vector(self.columns // 2 - 1, self.rows // 2),
            vector(self.columns // 2 - 2, self.rows // 2)
        ]
        self.directions = {
            'Up': vector(0, -1),
            'Right': vector(1, 0),
            'Down': vector(0, 1),
            'Left': vector(-1, 0),
        }
        self.current_direction = self.directions['Right']
        self.head = self.body[0]
        self.eaten_food = False
    
    def draw(self, surface: pg.Surface) -> None:
        for body_part in self.body:
            rect = pg.Rect(body_part.x * self.cell_size,
                           body_part.y * self.cell_size,
                           self.cell_size,
                           self.cell_size)
            pg.draw.rect(surface, self.color, rect, width=2)
    
    def check_valid_keys(self, keys_pressed: deque=None) -> bool:
        if keys_pressed:
            if self.current_direction == self.directions['Up'] and keys_pressed[0] == self.directions['Down']:
                return False
            elif self.current_direction == self.directions['Right'] and keys_pressed[0] == self.directions['Left']:
                return False
            elif self.current_direction == self.directions['Down'] and keys_pressed[0] == self.directions['Up']:
                return False
            elif self.current_direction == self.directions['Left'] and keys_pressed[0] == self.directions['Right']:
                return False
            else:
                return True
    
    def move(self, keys_pressed: deque=None) -> None:
        if self.check_valid_keys(keys_pressed):
            self.current_direction = keys_pressed[0]
            keys_pressed.popleft()

        new_head = self.body[0] + self.current_direction
        if not self.eaten_food:
            self.body = [new_head] + self.body[:-1]
        else:
            self.body = [new_head] + self.body[:]
            self.eaten_food = False
