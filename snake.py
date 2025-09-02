from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Game

from pygame import Vector2 as vector
import pygame as pg
from collections import deque

class Snake:
    def __init__(self, color: tuple[int, int, int]=(75, 0, 130), game: Game=None) -> None:
        self.game = game
        self.body = [
            vector(self.game.columns // 2, self.game.rows // 2),
            vector(self.game.columns // 2 - 1, self.game.rows // 2),
            vector(self.game.columns // 2 - 2, self.game.rows // 2)
        ]
        self.color = color
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
            rect = pg.Rect(body_part.x * self.game.cell_size,
                           body_part.y * self.game.cell_size,
                           self.game.cell_size,
                           self.game.cell_size)
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
