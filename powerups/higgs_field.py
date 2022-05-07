import pygame as pg

from constants import consts as c
from anims.ripple_generator import RippleGenerator

class HiggsField:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.radius = c.higgs_radius
        self.ripple_generator = RippleGenerator(x, y, 0.1 * c.higgs_radius, c.higgs_radius, 0.4 * c.higgs_radius, 50, c.ripples_color, screen)

    def outside_screen(self):
        return self.x < -c.higgs_radius

    def update(self):
        self.x -= c.scroll_speed * c.dt
        self.ripple_generator.move(self.x, self.y)
        self.ripple_generator.update()

    def render(self):
        self.ripple_generator.render()