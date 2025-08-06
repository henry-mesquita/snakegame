import settings
import pygame as pg
import random
from pygame import Vector2 as vector

class Food:
    def __init__(self, color, game):
        self.game = game
        self.color = color
        self.pos = self.get_random_pos()
    
    def draw(self, screen):
        rect = pg.Rect(self.pos[0] * settings.CELL_SIZE,
                       self.pos[1] * settings.CELL_SIZE,
                       settings.CELL_SIZE,
                       settings.CELL_SIZE)
        pg.draw.rect(screen, self.color, rect, width=2)
    
    def get_random_pos(self):
        if len(self.game.snake.body) == settings.ROWS * settings.COLUMNS:
            self.game.game_running = False
            return vector(-1, -1)
        
        while True:
            x = random.randint(0, settings.ROWS - 1)
            y = random.randint(0, settings.COLUMNS - 1)
            pos_ok = True
            for body_part in self.game.snake.body:
                if body_part.x == x and body_part.y == y:
                    pos_ok = False
                    break
            if pos_ok:
                return vector(x, y)
