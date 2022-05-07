from math import ceil, pi
import pygame as pg

from constants import consts as c
from anims.revolve import Revolve
from anims.ripple_generator import RippleGenerator


class Player:

    def __init__(self, mass, matter, screen):
        self.mass = mass
        self.matter = matter
        self.screen = screen

        if matter == "normal":
            self.nucleus_color = c.normal_nucleus_color
            self.electron_color = c.normal_electron_color
        else:
            self.nucleus_color = c.anti_nucleus_color
            self.electron_color = c.anti_electron_color

        self.x = c.screen_width / 5
        self.y = c.screen_height / 2

        self.revolve = Revolve(self.x, self.y, 0, c.electron_radius,
                               self.electron_color, self.screen)
        self.ripple_generator = RippleGenerator(self.x, self.y,
                                                3 * c.max_nuclear_radius,
                                                1.1 * c.max_nuclear_radius,
                                                2.33 * c.max_nuclear_radius,
                                                50, c.ripples_color, screen)
        self.calculate_radius()

        self.energy = 100
        self.converting_mass_to_energy = False
        self.convert_energy_cycle = 0

        self.alive = True

    def reset_position(self):
        self.x = c.screen_width / 5
        self.y = c.screen_height / 2

    def change_matter(self):
        if self.matter == "normal":
            self.matter = "anti"
        else:
            self.matter = "normal"

        if self.matter == "normal":
            self.nucleus_color = c.normal_nucleus_color
            self.electron_color = c.normal_electron_color
        else:
            self.nucleus_color = c.anti_nucleus_color
            self.electron_color = c.anti_electron_color

        self.mass = c.max_mass
        self.calculate_radius()
        self.energy = c.max_energy
        self.alive = True
        self.revolve.color = self.electron_color

    def update(self, keys_pressed):
        if self.alive:
            front_speed, back_speed, vertical_speed = 0, 0, 0
            if self.num_electrons > 0:
                front_speed = c.atom_speed_front
                back_speed = c.atom_speed_back
                vertical_speed = c.atom_speed_vertical
            else:
                front_speed = c.nucleus_speed_front
                back_speed = c.nucleus_speed_back
                vertical_speed = c.nucleus_speed_vertical

            if keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]:
                self.x -= back_speed * c.dt
            if keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]:
                self.x += front_speed * c.dt
            if keys_pressed[pg.K_UP] or keys_pressed[pg.K_w]:
                self.y -= vertical_speed * c.dt
            if keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_s]:
                self.y += vertical_speed * c.dt

            if self.converting_mass_to_energy:
                self.increase_energy(c.max_energy / c.energy_increase_cycle)
                self.convert_energy_cycle += 1

                if self.convert_energy_cycle == c.energy_increase_cycle:
                    self.convert_energy_cycle = 0
                    self.converting_mass_to_energy = False
            else:
                energy_increase = c.energy_replenish_rate * c.dt
                if self.num_electrons > 0:
                    self.increase_energy(c.atom_rate_multiplicative * energy_increase)
                else:
                    self.increase_energy(energy_increase)
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
        if self.alive:
            pg.draw.circle(self.screen, self.nucleus_color,
                           (int(self.x), int(self.y)), int(self.radius))
            self.revolve.render()
            self.ripple_generator.render()

    def increase_mass(self, mass):
        self.mass += mass
        if self.mass >= c.max_mass:
            self.mass = c.max_mass
        self.calculate_radius()

    def decrease_mass(self, mass):
        self.mass -= mass
        if self.mass < 0:
            self.alive = False
            self.radius = 0
        else:
            self.calculate_radius()

    def increase_energy(self, energy):
        self.energy += energy
        if self.energy > c.max_energy:
            self.energy = c.max_energy

    def decrease_energy(self, energy):
        self.energy -= energy
        if self.energy < 0:
            if self.mass > c.mass_energy_refill:
                self.decrease_mass(c.mass_energy_refill)
                self.converting_mass_to_energy = True

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
        if self.mass > c.max_nucleons * c.nucleon_mass:
            self.nuclear_mass = c.max_nucleons * c.nucleon_mass
            self.total_electron_mass = self.mass - self.nuclear_mass
            self.num_electrons = ceil(self.total_electron_mass /
                                     c.electron_mass)
        else:
            self.nuclear_mass = self.mass
            self.num_electrons = 0

        self.radius = pow(self.nuclear_mass / (4 * pi * c.density), 1 / 3)
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