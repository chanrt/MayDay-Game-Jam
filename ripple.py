import pygame as pg


class Ripple:
    def __init__(self, x, y, start_radius, end_radius, color, screen):
        self.x = x
        self.y = y
        self.start_radius = start_radius
        self.end_radius = end_radius
        self.color = color
        self.screen = screen
        
        self.display = True
        
        if start_radius < end_radius:
            self.inwards = False
        else:
            self.inwards = True

        self.radius = start_radius
        self.speed = 2
        self.max_thickness = 3
        self.min_thickness = 1

        self.slope = (self.max_thickness - self.min_thickness) / (self.start_radius - self.end_radius)

        if self.inwards:
            self.thickness = self.min_thickness
        else:
            self.thickness = self.max_thickness

    def update(self):
        if self.inwards:
            self.radius -= self.speed
            if self.radius <= self.end_radius:
                self.display = False
        else:
            self.radius += self.speed
            if self.radius >= self.end_radius:
                self.display = False
        self.thickness += self.slope * self.speed

    def render(self):
        if self.display:
            pg.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), int(self.radius), int(self.thickness))