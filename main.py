import pygame as pg
from pygame import Vector2 as vector
from snake import Snake
from food import Food
from menu import show_config_menu
from collections import deque
import random

class Game:
    def __init__(
            self,
            board_size:     int=15,
            cell_size:      int=30,
            snake_speed:    int=150
    ) -> None:
        """
        Initialize the game.

        Args:
            board_size (int, optional): The size of the game board. Defaults to 15.
            cell_size (int, optional): The size of each cell on the game board. Defaults to 30.
            snake_speed (int, optional): The speed of the snake. Defaults to 150.
        Returns:
            None
        """
        # GAME CONFIG
        self.FRAMERATE              = 60
        self.GREEN                  = (0, 255, 0)
        self.WHITE                  = (255, 255, 255)
        self.BLACK                  = (0, 0, 0)
        self.RED                    = (255, 0, 0)
        self.DARK_PURPLE            = (75, 0, 130)
        self.GREY                   = (240, 240, 240)
        self.DARK_GREY              = (170, 170, 170)

        # BOARD CONFIG
        self.board_size         = board_size
        self.cell_size          = cell_size
        self.rows, self.columns = board_size, board_size
        self.screen_dim         = (self.columns * self.cell_size, self.columns * self.cell_size)

        # GAME INSTANCES
        self.snake = Snake(self.DARK_PURPLE, self.cell_size, self.columns, self.rows)
        self.food = Food(self.RED, self.cell_size, self.columns, self.rows)

        self.INITIAL_SNAKE_LENGTH   = len(self.snake.body)

        # SNAKE SPEED
        self.snake_speed = snake_speed

        # PYGAME SETUP
        pg.display.set_caption('Snake Game')
        self.font = pg.font.Font(None, 20)
        self.screen = pg.display.set_mode(self.screen_dim)
        self.clock = pg.time.Clock()

        # GAME SETUP
        self.last_move_time = 0
        self.score = 0
        self.food_pos = self.get_random_pos()
        self.keys_pressed = deque(maxlen=2)
    
    def draw_text(self, info: str, x: int=10, y: int=10) -> None:
        """
        Draw text on the screen.

        Args:
            info (str): The text to be drawn.
            x (int, optional): The x position of the text. Defaults to 10.
            y (int, optional): The y position of the text. Defaults to 10.
        Returns:
            None
        """
        debug_surface = self.font.render(str(info), True, 'Green')
        debug_rect = debug_surface.get_rect(topleft=(x, y))
        pg.draw.rect(self.screen, 'white', debug_rect)
        self.screen.blit(debug_surface, debug_rect)

    def draw_grid(self) -> None:
        """
        Draw a grid on the screen.
        Returns:
            None
        """
        for x in range(0, self.screen_dim[0], self.cell_size):
            pg.draw.line(self.screen, self.GREY, (x, 0), (x, self.screen_dim[1]), width=3)
        for y in range(0, self.screen_dim[1], self.cell_size):
            pg.draw.line(self.screen, self.GREY, (0, y), (self.screen_dim[0], y), width=3)
    
    def check_eaten_food(self) -> bool:
        """
        Check if the snake has eaten the food.
        Returns:
            bool: True if the snake has eaten the food, False otherwise.
        """
        if self.snake.head == self.food_pos:
            return True

    def check_death(self) -> bool:
        """
        Check if the snake has died.
        Returns:
            bool: True if the snake has died, False otherwise.
        """
        body_collision = self.snake.head in self.snake.body[1:]
        border_x_collision = (self.snake.head.x < 0 or self.snake.head.x * self.cell_size >= self.screen_dim[0])
        border_y_collision = (self.snake.head.y < 0 or self.snake.head.y * self.cell_size >= self.screen_dim[1])
        
        if body_collision or border_x_collision or border_y_collision:
            return True
        return False

    def process_movement(self) -> None:
        """
        Process the movement of the snake.
        Returns:
            None
        """
        if self.current_time - self.last_move_time > self.snake_speed:
            self.last_move_time = self.current_time
            self.snake.move(self.keys_pressed)
            self.snake.head = self.snake.body[0]

            if self.check_eaten_food():
                self.score += 1
                self.food_pos = self.get_random_pos()
                self.snake.eaten_food = True

        if self.check_death():
            self.game_running = False

    def event_loop(self) -> None:
        """
        Handle events.
        Returns:
            None
        """
        key_map = {
            pg.K_UP:    self.snake.directions['Up'],
            pg.K_RIGHT: self.snake.directions['Right'],
            pg.K_DOWN:  self.snake.directions['Down'],
            pg.K_LEFT:  self.snake.directions['Left']
        }

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game_running = False
            elif event.type == pg.KEYDOWN:
                if event.key in key_map:
                    self.keys_pressed.append(key_map[event.key])
    
    def check_win(self) -> bool:
        """
        Check if the player has won the game.
        Returns:
            bool: True if the player has won the game, False otherwise.
        """
        if self.score == self.rows * self.columns - self.INITIAL_SNAKE_LENGTH:
            return True
        else:
            return False
    
    def get_random_pos(self) -> vector:
        """
        Get a random position for the food.
        Returns:
            vector: The position of the food.
        """
        while True:
            x = random.randint(0, self.columns - 1)
            y = random.randint(0, self.rows - 1)
            pos_ok = True
            for body_part in self.snake.body:
                if body_part.x == x and body_part.y == y:
                    pos_ok = False
                    break
            if pos_ok:
                return vector(x, y)

    def run(self) -> None:
        """
        Run the game (game loop).
        Returns:
            None
        """
        self.game_running = True
        while self.game_running: # GAME LOOP
            self.current_time = pg.time.get_ticks()

            if self.check_win():
                self.game_running = False

            self.event_loop()
            self.process_movement()

            self.screen.fill(self.WHITE)
            self.draw_grid()
            self.snake.draw(self.screen)
            self.food.draw(self.screen, self.food_pos)

            pg.display.update()
            self.clock.tick(self.FRAMERATE)

def main() -> None:
    pg.init()
    while True:
        try:
            board_size, cell_size, snake_speed, game_running = show_config_menu()
            if game_running == True:
                game = Game(board_size, cell_size, snake_speed)
                game.run()
            else:
                break
        except Exception as e:
            print(f'Exception: {e}')
    pg.quit()

if __name__ == '__main__':
    main()
