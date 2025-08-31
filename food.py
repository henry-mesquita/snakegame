from __future__ import annotations
import pygame as pg
import random
from pygame import Vector2 as vector


class Food:
    def __init__(self, color: tuple=(255, 0, 0), game: Game=None) -> None:
        self.game = game
        self.color = color
        self.pos = self.get_random_pos()
    
    def draw(self, screen: pg.Surface=None) -> None:
        rect = pg.Rect(self.pos[0] * self.game.cell_size,
                       self.pos[1] * self.game.cell_size,
                       self.game.cell_size,
                       self.game.cell_size)
        pg.draw.rect(screen, self.color, rect, width=2)
    
    def get_random_pos(self) -> vector:
        while True:
            x = random.randint(0, self.game.columns - 1)
            y = random.randint(0, self.game.rows - 1)
            pos_ok = True
            for body_part in self.game.snake.body:
                if body_part.x == x and body_part.y == y:
                    pos_ok = False
                    break
            if pos_ok:
                return vector(x, y)
