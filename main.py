import pygame as pg
from pygame import Vector2 as vector
from snake import Snake
from food import Food
from menu import show_config_menu
from collections import deque

class Game:
    def __init__(self, board_size=15, cell_size=30, snake_speed=150):
        pg.init()
        pg.display.set_caption('Snake Game')

        self.FRAMERATE = 60
        self.GREEN = (0, 255, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.DARK_PURPLE = (75, 0, 130)
        self.GREY = (240, 240, 240)
        self.DARK_GREY = (170, 170, 170)

        self.snake_speed = snake_speed
        self.board_size = board_size
        self.cell_size = cell_size
        self.rows, self.columns = board_size, board_size
        self.screen_dim = (self.columns * self.cell_size, self.columns * self.cell_size)

        self.screen = pg.display.set_mode(self.screen_dim)
        self.clock = pg.time.Clock()

        self.snake = Snake(self.DARK_PURPLE, self)
        self.food = Food(self.RED, self)
        self.last_move_time = 0
        self.score = 0

        self.keys_pressed = deque(maxlen=2)

    def draw_grid(self):
        for x in range(0, self.screen_dim[0], self.cell_size):
            pg.draw.line(self.screen, self.GREY, (x, 0), (x, self.screen_dim[1]), width=3)
        for y in range(0, self.screen_dim[1], self.cell_size):
            pg.draw.line(self.screen, self.GREY, (0, y), (self.screen_dim[0], y), width=3)
    
    def check_eaten_food(self):
        if self.snake.head == self.food.pos:
            return True

    def check_death(self):
        body_collision = self.snake.head in self.snake.body[1:]
        border_x_collision = (self.snake.head.x < 0 or self.snake.head.x * self.cell_size >= self.screen_dim[0])
        border_y_collision = (self.snake.head.y < 0 or self.snake.head.y * self.cell_size >= self.screen_dim[1])
        
        if body_collision or border_x_collision or border_y_collision:
            return True
        return False

    def process_movement(self):
        if self.current_time - self.last_move_time > self.snake_speed:
            self.last_move_time = self.current_time
            self.snake.move(self.keys_pressed)
            self.snake.head = self.snake.body[0]

            if self.check_eaten_food():
                self.score += 1
                self.food.pos = self.food.get_random_pos()
                self.snake.eaten_food = True

        if self.check_death():
            self.game_running = False

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game_running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.keys_pressed.append(self.snake.directions['Up'])
                elif event.key == pg.K_RIGHT:
                    self.keys_pressed.append(self.snake.directions['Right'])
                elif event.key == pg.K_DOWN:
                    self.keys_pressed.append(self.snake.directions['Down'])
                elif event.key == pg.K_LEFT:
                    self.keys_pressed.append(self.snake.directions['Left'])

    def run(self):
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
            self.food.draw(self.screen)

            pg.display.update()
            self.clock.tick(self.FRAMERATE)
    
    def check_win(self):
        if self.score == self.rows * self.columns - 3:
            return True
        else:
            return False

def main():
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
