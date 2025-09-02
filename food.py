import pygame as pg
import random
from pygame import Vector2 as vector

class Food:
    def __init__(
            self,
            color: tuple[int, int, int]=(255, 0, 0),
            cell_size: int=None,
            columns: int=None,
            rows: int=None,
            body_parts: list[vector]=None
        ) -> None:

        self.color = color
        self.cell_size = cell_size
        self.columns = columns
        self.rows = rows
        self.body_parts = body_parts
        self.pos = self.get_random_pos()
    
    def draw(self, screen: pg.Surface=None) -> None:
        rect = pg.Rect(self.pos[0] * self.cell_size,
                       self.pos[1] * self.cell_size,
                       self.cell_size,
                       self.cell_size)
        pg.draw.rect(screen, self.color, rect, width=2)
    
    def get_random_pos(self) -> vector:
        while True:
            x = random.randint(0, self.columns - 1)
            y = random.randint(0, self.rows - 1)
            pos_ok = True
            for body_part in self.body_parts:
                if body_part.x == x and body_part.y == y:
                    pos_ok = False
                    break
            if pos_ok:
                return vector(x, y)
