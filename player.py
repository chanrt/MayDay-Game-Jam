from math import pi

import pygame as pg

from constants import consts as c
from revolve import Revolve
from ripple_generator import RippleGenerator

class Player:
    def __init__(self, mass, screen):
        self.mass = mass
        self.screen = screen

        self.x = c.screen_width / 10
        self.y = c.screen_height / 2
        
        self.revolve = Revolve(self.x, self.y, 0, c.electron_radius, pg.Color("white") , self.screen)
        self.ripple_generator = RippleGenerator(self.x, self.y, c.max_nuclear_radius, 3 * c.max_nuclear_radius, 1.66 * c.max_nuclear_radius, 0.5, pg.Color("green"), screen)
        self.calculate_radius()

    def update(self, keys_pressed):
        speed = 0
        if self.num_electrons > 0:
            speed = c.atom_speed
        else:
            speed = c.nucleus_speed

        if keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]:
            self.x -= speed
        if keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]:
            self.x += speed
        if keys_pressed[pg.K_UP] or keys_pressed[pg.K_w]:
            self.y -= speed
        if keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_s]:
            self.y += speed

        self.constrain_player()
        self.update_animations()

    def update_animations(self):
        if self.revolve.display:
            self.revolve.x = self.x
            self.revolve.y = self.y
            self.revolve.update()
        elif self.ripple_generator.display:
            self.ripple_generator.update()
            self.ripple_generator.move(self.x, self.y)

    def render(self):
        pg.draw.circle(self.screen, pg.Color("blue"), (int(self.x), int(self.y)), int(self.radius))
        self.revolve.render()
        self.ripple_generator.render()

    def increase_mass(self, mass):
        self.mass += mass
        if self.mass > c.max_mass:
            self.mass = c.max_mass
        self.calculate_radius()

    def decrease_mass(self, mass):
        self.mass -= mass
        self.calculate_radius()

    def lose_electrons(self):
        self.mass = self.mass - self.num_electrons * c.electron_mass
        self.calculate_radius()

    def decide_animation(self):
        if self.num_electrons == 0:
            self.ripple_generator.display = True
        else:
            self.ripple_generator.display = False
            self.ripple_generator.clear_ripples()
        
        if self.num_electrons > 0:
            self.revolve.display = True
            self.revolve.orbit_radius = 2 * self.radius
            self.revolve.set_num_particles(self.num_electrons)
        else:
            self.revolve.display = False

    def calculate_radius(self):
        if self.mass >= c.max_nucleons * c.nucleon_mass:
            self.nuclear_mass = c.max_nucleons * c.nucleon_mass
            self.total_electron_mass = self.mass - self.nuclear_mass
            self.num_electrons = int(self.total_electron_mass / c.electron_mass)
        else:
            self.nuclear_mass = self.mass
            self.num_electrons = 0

        self.radius = pow(self.nuclear_mass / (4 * pi * c.density), 1/3)
        self.decide_animation()

    def constrain_player(self):
        if self.x - self.radius < c.horizontal_constrain:
            self.x = c.horizontal_constrain + self.radius
        elif self.x + self.radius > c.screen_width - c.horizontal_constrain:
            self.x = c.screen_width - c.horizontal_constrain - self.radius

        if self.y - self.radius < c.vertical_constrain:
            self.y = c.vertical_constrain + self.radius
        elif self.y + self.radius > c.screen_height - c.vertical_constrain:
            self.y = c.screen_height - c.vertical_constrain - self.radius