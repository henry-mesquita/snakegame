import pygame as pg, settings
from pygame import Vector2 as vector
from snake import Snake
from food import Food

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Snake Game')

        self.screen = pg.display.set_mode(settings.SCREEM_DIM)
        self.clock = pg.time.Clock()
        self.snake = Snake(settings.DARK_PURPLE, self)
        self.food = Food(settings.RED, self)
        self.key_pressed = False
        self.score = 0
    
    def draw_grid(self):
        for x in range(0, settings.SCREEM_DIM[0], settings.CELL_SIZE):
            pg.draw.line(self.screen, settings.DARK_GREY, (x, 0), (x, settings.SCREEM_DIM[1]))
        for y in range(0, settings.SCREEM_DIM[1], settings.CELL_SIZE):
            pg.draw.line(self.screen, settings.DARK_GREY, (0, y), (settings.SCREEM_DIM[0], y))
    
    def process_movement(self):
            if self.current_time - self.last_move_time > settings.SNAKE_SPEED:
                self.last_move_time = self.current_time
                self.snake.move()
                self.snake.head = self.snake.body[0]

                if self.snake.check_eaten_food():
                    self.score += 1
                    self.food.pos = self.food.get_random_pos()
                    self.snake.eaten_food = True

            if self.snake.check_death():
                self.running = False

    def run(self):
        self.running = True
        self.last_move_time = 0

        while self.running: # GAME LOOP
            self.current_time = pg.time.get_ticks()

            for event in pg.event.get(): # EVENT LOOP
                if event.type == pg.QUIT:
                    self.running = False
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

            self.screen.fill(settings.WHITE)
            self.draw_grid()
            self.snake.draw(self.screen)
            self.food.draw(self.screen)

            pg.display.update()
            self.clock.tick(settings.FRAMERATE)
        pg.quit()

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
