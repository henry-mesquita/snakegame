from pygame import Vector2
import pygame as pg
from collections import deque
from typing import Optional

class Snake:
    def __init__(
            self,
            cell_size:  int,
            columns:    int,
            rows:       int,
            color:      Optional[tuple[int, int, int]]=(75, 0, 130)
        ) -> None:
        """
        Initialize the snake.

        Args:
            color (tuple[int, int, int], optional): The color of the snake. Defaults to (75, 0, 130).
            cell_size (int): The size of each cell on the game board. Defaults to None.
            columns (int): The number of columns in the game board. Defaults to None.
            rows (int): The number of rows in the game board. Defaults to None.
        Returns:
            None
        """
        self.color: tuple[int, int, int]    = color
        self.cell_size: int                 = cell_size
        self.columns: int                   = columns
        self.rows: int                      = rows
        self.body: list[Vector2] = [
            Vector2(self.columns // 2, self.rows // 2),
            Vector2(self.columns // 2 - 1, self.rows // 2),
            Vector2(self.columns // 2 - 2, self.rows // 2)
        ]
        self.directions = {
            'Up': Vector2(0, -1),
            'Right': Vector2(1, 0),
            'Down': Vector2(0, 1),
            'Left': Vector2(-1, 0),
        }
        self.current_direction: Vector2 = self.directions['Right']
        self.head: Vector2 = self.body[0]
        self.eaten_food: bool = False
    
    def draw(self, surface: pg.Surface) -> None:
        """
        Draw the snake on the screen.

        Args:
            surface (pg.Surface): The surface to draw on. Defaults to None.
        Returns:
            None
        """
        for body_part in self.body:
            rect = pg.Rect(body_part.x * self.cell_size,
                           body_part.y * self.cell_size,
                           self.cell_size,
                           self.cell_size)
            pg.draw.rect(surface, self.color, rect, width=2)
    
    def check_valid_keys(
            self,
            keys_pressed: Optional[deque]=None
    ) -> bool:
        """
        Check if the keys pressed are valid.

        Args:
            keys_pressed (deque, optional): The keys pressed. Defaults to None.
        Returns:
            bool: True if the keys pressed are valid, False otherwise.
        """
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
    
    def move(
            self,
            keys_pressed: Optional[deque]=None
    ) -> None:
        """
        Move the snake.

        Args:
            keys_pressed (deque, optional): The keys pressed. Defaults to None.
        Returns:
            None
        """
        if self.check_valid_keys(keys_pressed):
            self.current_direction = keys_pressed[0]
            keys_pressed.popleft()

        new_head = self.body[0] + self.current_direction
        if not self.eaten_food:
            self.body = [new_head] + self.body[:-1]
        else:
            self.body = [new_head] + self.body[:]
            self.eaten_food = False
