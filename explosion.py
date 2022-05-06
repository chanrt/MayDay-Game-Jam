from math import cos, pi, sin
from random import random

import pygame as pg


class Particle:
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

    def update(self):
        noise = 1 * random() - 0.5
        self.x += cos(self.theta + noise)
        self.y += sin(self.theta + noise)
    

class Explosion:
    def __init__(self, x, y, explosion_radius, color, screen):
        self.x = x
        self.y = y
        self.radius = explosion_radius
        self.color = color
        self.screen = screen

        self.display = True
        self.num_particles = 50
        self.max_particle_size = 3

        self.current_step = 0
        self.final_step = 100

        self.make_particles()

    def make_particles(self):
        self.particles = []

        for i in range(self.num_particles):
            theta = 2 * pi * random()
            r = self.radius * random()
            x = self.x + r * cos(theta)
            y = self.y + r * sin(theta)

            self.particles.append(Particle(x, y, theta))

    def update(self):
        for particle in self.particles:
            particle.update()

        self.current_step += 1
        if self.current_step >= self.final_step:
            self.display = False

    def render(self):
        if self.display:
            for particle in self.particles:
                pg.draw.circle(self.screen, self.color, (particle.x, particle.y), self.max_particle_size * (1 - self.current_step / self.final_step), 0)