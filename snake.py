from pygame import Vector2 as vector
import pygame as pg

class Snake:
    def __init__(self, color, game):
        self.game = game
        self.body = [
            vector(self.game.columns // 2, self.game.rows // 2),
            vector((self.game.columns // 2) - 1, self.game.rows // 2),
            vector((self.game.columns // 2) - 2, self.game.rows // 2)
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
    
    def draw(self, screen):
        for body_part in self.body:
            rect = pg.Rect(body_part.x * self.game.cell_size,
                           body_part.y * self.game.cell_size,
                           self.game.cell_size,
                           self.game.cell_size)
            pg.draw.rect(screen, self.color, rect, width=2)
    
    def move(self, keys_pressed):
        if keys_pressed:
            self.current_direction = keys_pressed[0]
            keys_pressed.popleft()

        new_head = self.body[0] + self.current_direction
        if not self.eaten_food:
            self.body = [new_head] + self.body[:-1]
        else:
            self.body = [new_head] + self.body[:]
            self.eaten_food = False
