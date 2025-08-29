import pygame as pg
from pygame import Vector2 as vector
from snake import Snake
from food import Food
from menu import show_config_menu

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
        self.key_pressed = False
        self.score = 0

    def draw_grid(self):
        for x in range(0, self.screen_dim[0], self.cell_size):
            pg.draw.line(self.screen, self.GREY, (x, 0), (x, self.screen_dim[1]), width=3)
        for y in range(0, self.screen_dim[1], self.cell_size):
            pg.draw.line(self.screen, self.GREY, (0, y), (self.screen_dim[0], y), width=3)
    
    def process_movement(self):
            if self.current_time - self.last_move_time > self.snake_speed:
                self.last_move_time = self.current_time
                self.snake.move()
                self.snake.head = self.snake.body[0]

                if self.snake.check_eaten_food():
                    self.score += 1
                    self.food.pos = self.food.get_random_pos()
                    self.snake.eaten_food = True

            if self.snake.check_death():
                self.game_running = False

    def run(self):
        self.snake = Snake(self.DARK_PURPLE, self)
        self.food = Food(self.RED, self)
        self.game_running = True
        self.last_move_time = 0
        self.score = 0

        while self.game_running: # GAME LOOP
            self.current_time = pg.time.get_ticks()

            for event in pg.event.get(): # EVENT LOOP
                if event.type == pg.QUIT:
                    self.game_running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP and not self.key_pressed:
                        if self.snake.current_direction != vector(0, 1):
                            self.snake.current_direction = self.snake.directions['Up']
                            self.key_pressed = True
                    elif event.key == pg.K_RIGHT and not self.key_pressed:
                        if self.snake.current_direction != vector(-1, 0):
                            self.key_pressed = True
                            self.snake.current_direction = self.snake.directions['Right']
                    elif event.key == pg.K_DOWN and not self.key_pressed:
                        if self.snake.current_direction != vector(0, -1):
                            self.key_pressed = True
                            self.snake.current_direction = self.snake.directions['Down']
                    elif event.key == pg.K_LEFT and not self.key_pressed:
                        if self.snake.current_direction != vector(1, 0):
                            self.key_pressed = True
                            self.snake.current_direction = self.snake.directions['Left']
            
            self.process_movement()

            self.screen.fill(self.WHITE)
            self.draw_grid()
            self.snake.draw(self.screen)
            self.food.draw(self.screen)

            pg.display.update()
            self.clock.tick(self.FRAMERATE)
    
    def check_win(self):
        if self.score == self.rows * self.rows - 3:
            return True

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
