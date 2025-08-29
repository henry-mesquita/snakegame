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
    
    def move(self):
        if self.game.check_win():
            self.game.game_running = False
            return self.game.end_menu()
        new_head = self.body[0] + self.current_direction
        if not self.eaten_food:
            self.body = [new_head] + self.body[:-1]
        else:
            self.body = [new_head] + self.body[:]
            self.eaten_food = False
        self.game.key_pressed = False

    def check_death(self):
        body_collision = self.head in self.body[1:]
        border_x_collision = (self.head.x < 0 or self.head.x * self.game.cell_size >= self.game.screen_dim[0])
        border_y_collision = (self.head.y < 0 or self.head.y * self.game.cell_size >= self.game.screen_dim[1])
        
        if body_collision or border_x_collision or border_y_collision:
            return True
        return False

    def check_eaten_food(self):
        if self.head == self.game.food.pos:
            return True
