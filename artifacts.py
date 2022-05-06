import pygame as pg

from constants import consts as c


class Artifact:
    def __init__(self, y, screen):
        self.x = c.screen_width
        self.y = y
        self.screen = screen
        self.rect = pg.Rect(self.x, self.y, c.artifact_width, c.artifact_height)

    def outside_screen(self):
        if self.x < -self.rect.width:
            return True

    def update(self):
        self.x -= c.scroll_speed * c.dt
        self.rect = pg.Rect(self.x, self.y, c.artifact_width, c.artifact_height)

    def render(self):
        pg.draw.rect(self.screen, c.artifact_color, self.rect)