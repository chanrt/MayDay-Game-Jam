from math import pi

class Constants:
    def __init__(self):
        self.density = 0.0001

        self.nucleon_mass = 1
        self.electron_mass = 0.2
        self.electron_radius = 6

        self.max_nucleons = 6
        self.max_electrons = 6

        self.max_nuclear_radius = pow(self.max_nucleons * self.nucleon_mass / (4 * pi * self.density), 1/3)
        self.max_mass = self.max_nucleons * self.nucleon_mass + self.max_electrons * self.electron_mass

        self.atom_speed = 5
        self.nucleus_speed = 8

        self.horizontal_constrain = 50

    def set_screen_size(self, screen):
        self.screen_width, self.screen_height = screen.get_size()
        self.border_thickness = self.screen_height / 20

consts = Constants()