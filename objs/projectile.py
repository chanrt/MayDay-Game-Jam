from math import cos, sin
import pygame as pg

from constants import consts as c

class Projectile:
    def __init__(self, x, y, theta, color, screen):
        self.x = x
        self.y = y
        self.color = color
        self.theta = theta

        self.screen = screen
        self.active = True

    def change_matter(self):
        if self.color == c.normal_nucleus_color:
            self.color = c.anti_nucleus_color
        else:
            self.color = c.normal_nucleus_color

    def update(self):
        self.x += c.projectile_speed * c.dt * cos(self.theta)
        self.y += c.projectile_speed * c.dt * sin(self.theta)

    def render(self):
        pg.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), c.projectile_radius, 0)

    def outside_screen(self):
        return self.x < 0 or self.x > c.screen_width or self.y < 0 or self.y > c.screen_height