import pygame as pg
from random import random

from constants import consts as c


class Artifact:
    def __init__(self, y, screen):
        self.x = c.screen_width
        self.y = y
        self.screen = screen
        self.rect = pg.Rect(self.x, self.y, c.artifact_width, c.artifact_height)

        self.current_slide_speed = c.artifact_slide_speed if random() < 0.5 else -c.artifact_slide_speed

    def outside_screen(self):
        if self.x < -self.rect.width:
            return True

    def update(self):
        self.x -= c.scroll_speed * c.dt
        self.y += self.current_slide_speed * c.dt

        if self.y < 0:
            self.current_slide_speed *= -1
            self.y = 0
        elif self.y + c.artifact_height > c.screen_height:
            self.current_slide_speed *= -1
            self.y = c.screen_height - c.artifact_height

        self.rect = pg.Rect(self.x, self.y, c.artifact_width, c.artifact_height)

    def render(self):
        pg.draw.rect(self.screen, c.artifact_color, self.rect)