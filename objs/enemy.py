from math import pi
import pygame as pg

from constants import consts as c


class Enemy:

    def __init__(self, y, mass, matter, screen):
        self.x = c.screen_width + 20 * c.artifact_width
        self.y = y
        self.init_mass = mass
        self.mass = mass
        self.matter = matter
        self.screen = screen

        self.calculate_radius()
        self.init_color()

        self.alive = True
        self.fire_cycle = 0

    def init_color(self):
        if self.matter == "normal":
            self.color = c.normal_nucleus_color
        else:
            self.color = c.anti_nucleus_color

    def change_matter(self):
        if self.matter == "normal":
            self.matter = "anti"
        else:
            self.matter = "normal"
        self.init_color()

    def take_damage(self, damage):
        self.mass -= damage
        if self.mass < 0:
            self.alive = False
            self.radius = 0
        else:
            self.calculate_radius()
        
    def calculate_radius(self):
        self.radius = pow(self.mass / (4 * pi * c.enemy_density), 1 / 3)

    def should_dodge(self, player, artifact):
        if artifact.y < self.y + 2 * self.radius and self.y - 2 * self.radius < artifact.y + c.artifact_height:
            if artifact.x < player.x and player.x < self.x:
                return False
            else:
                return True
        else:
            return False

    def update(self, player, artifacts, dt):
        self.fire_cycle -= dt

        artifacts_in_front = list(filter(lambda a: a.x < self.x, artifacts))
        artifacts_in_front.sort(key=lambda a: a.x)

        if len(artifacts_in_front) > 0:
            next_artifact = artifacts_in_front[-1]
        else:
            next_artifact = None

        if next_artifact is not None and self.should_dodge(player, next_artifact):
            self.x -= (c.scroll_speed + c.enemy_speed) * c.dt
            if (self.y - next_artifact.y) < (next_artifact.y + c.artifact_height - self.y):
                self.y -= c.enemy_speed * c.dt
            else:
                self.y += c.enemy_speed * c.dt
        elif player.x < self.x:
            self.x -= c.scroll_speed * c.dt
            if abs(player.x - self.x) > c.enemy_speed * c.dt:
                if self.x > player.x:
                    self.x -= c.enemy_speed * c.dt
                else:
                    self.x += c.enemy_speed * c.dt
            if abs(player.y - self.y) > c.enemy_speed * c.dt:
                if self.y > player.y:
                    self.y -= c.enemy_speed * c.dt
                else:
                    self.y += c.enemy_speed * c.dt
        else:
            self.x -= (c.scroll_speed + c.enemy_speed) * c.dt

    def outside_screen(self):
        if self.x < -self.radius:
            return True
        
    def render(self):
        pg.draw.circle(self.screen, c.halo_color, (int(self.x), int(self.y)), int(self.radius) + c.halo_thickness)
        pg.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), int(self.radius))