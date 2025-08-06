import pygame as pg, settings
from pygame import Vector2 as vector
from snake import Snake
from food import Food
from button import Button

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Snake Game')

        self.screen = pg.display.set_mode(settings.SCREEN_DIM)
        self.clock = pg.time.Clock()
        self.key_pressed = False
        self.score = 0

    def menu(self):
        self.menu_running = True
        self.start_btn = Button(text='Start Game', width=200, height=40,
                                pos=(settings.SCREEN_DIM[0] // 2,
                                     settings.SCREEN_DIM[1] // 2 - settings.SCREEN_DIM[1] // 10),
                                screen=self.screen)
        # self.settings_btn = Button(text='Settings', width=200, height=40,
        #                            pos=(settings.SCREEN_DIM[0] // 2,
        #                                settings.SCREEN_DIM[1] // 2),
        #                                screen=self.screen)
        self.quit_btn = Button(text='Quit', width=200, height=40,
                                   pos=(settings.SCREEN_DIM[0] // 2,
                                       settings.SCREEN_DIM[1] // 2 + settings.SCREEN_DIM[1] // 10),
                                       screen=self.screen)

        while self.menu_running:
            if self.start_btn.clicked():
                self.menu_running = False
                return self.run()

            for event in pg.event.get(): # EVENT LOOP
                if event.type == pg.QUIT or self.quit_btn.clicked():
                    self.menu_running = False

            self.screen.fill(settings.WHITE)
            self.start_btn.draw()
            # self.settings_btn.draw()
            self.quit_btn.draw()

            pg.display.update()
            self.clock.tick(settings.FRAMERATE)

    def draw_grid(self):
        for x in range(0, settings.SCREEN_DIM[0], settings.CELL_SIZE):
            pg.draw.line(self.screen, settings.GREY, (x, 0), (x, settings.SCREEN_DIM[1]), width=3)
        for y in range(0, settings.SCREEN_DIM[1], settings.CELL_SIZE):
            pg.draw.line(self.screen, settings.GREY, (0, y), (settings.SCREEN_DIM[0], y), width=3)
    
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
                self.game_running = False
                return self.menu() 

    def run(self):
        self.snake = Snake(settings.DARK_PURPLE, self)
        self.food = Food(settings.RED, self)
        self.game_running = True
        self.last_move_time = 0

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

            self.screen.fill(settings.WHITE)
            self.draw_grid()
            self.snake.draw(self.screen)
            self.food.draw(self.screen)

            pg.display.update()
            self.clock.tick(settings.FRAMERATE)

def main():
    game = Game()
    game.menu()
    pg.quit()

if __name__ == '__main__':
    main()
