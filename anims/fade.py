import pygame as pg
from constants import consts as c


class Fade:
    def __init__(self, from_alpha, to_alpha, speed, color, screen):
        self.from_alpha = from_alpha
        self.to_alpha = to_alpha
        self.speed = speed
        self.color = color
        self.screen = screen

        if from_alpha < to_alpha:
            self.fade_in = True
        else:
            self.fade_in = False

        self.display = True

        self.alpha = from_alpha

    def update(self):
        if self.fade_in:
            self.alpha += self.speed * c.dt
            if self.alpha >= self.to_alpha:
                self.display = False
        else:
            self.alpha -= self.speed * c.dt
            if self.alpha <= self.to_alpha:
                self.display = False

    def render(self):
        if self.display:
            fade_screen = pg.Surface(self.screen.get_size())
            fade_screen.fill(self.color)
            fade_screen.set_alpha(self.alpha)
            self.screen.blit(fade_screen, (0, 0))