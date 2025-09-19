import pygame as pg
from pygame import Vector2
from typing import Optional

class Food:
    def __init__(
            self,
            color: Optional[tuple[int, int, int]]=(255, 0, 0),
            cell_size: Optional[int]=30,
            columns: Optional[int]=15,
            rows: Optional[int]=15
        ) -> None:
        """
        Initialize the food.

        Args:
            color (tuple[int, int, int], optional): The color of the food. Defaults to (255, 0, 0).
            cell_size (int, optional): The size of each cell on the game board. Defaults to None.
            columns (int, optional): The number of columns in the game board. Defaults to None.
            rows (int, optional): The number of rows in the game board. Defaults to None.
        Returns:
            None
        """
        self.color: tuple[int, int, int] = color
        self.cell_size: int = cell_size
        self.columns: int = columns
        self.rows: int = rows
    
    def draw(self, screen: pg.Surface, pos: tuple[int, int]) -> None:
        """
        Draw the food on the screen.

        Args:
            screen (pg.Surface): The surface to draw on. Defaults to None.
            pos (tuple[int, int]): The position of the food. Defaults to None.
        Returns:
            None
        """
        rect = pg.Rect(pos[0] * self.cell_size,
                       pos[1] * self.cell_size,
                       self.cell_size,
                       self.cell_size)
        pg.draw.rect(screen, self.color, rect, width=2)
