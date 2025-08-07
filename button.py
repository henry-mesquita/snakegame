import pygame as pg

class Button:
    def __init__(self, text, width, height, fontsize, pos, screen):
        self.screen = screen
        
        # Main Attributes
        self.pressed = False
        self.font = pg.font.Font(None, fontsize)
        # Top rectangle
        self.top_rect = pg.Rect((0, 0), (width, height))
        self.top_rect.center = pos
        self.top_color = '#475F77'
        # Text
        self.text_surf = self.font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
    
    def draw(self):
        pg.draw.rect(self.screen, self.top_color, self.top_rect)
        self.screen.blit(self.text_surf, self.text_rect)
        self.clicked()
    
    def clicked(self):
        mouse_pos = pg.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0]:
                self.pressed = True
                return self.pressed
            else:
                if self.pressed:
                    self.pressed = False
                    return self.pressed
