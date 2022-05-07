
from constants import consts as c
from anims.ripple import Ripple

class Burst:
    def __init__(self, x, y, color, screen):
        self.x = x
        self.y = y
        self.color = color
        self.screen = screen

        self.ripple = Ripple(self.x, self.y, 0, c.screen_width, color, screen)
        self.ripple.thickness = 10
        self.ripple.speed = 1000
        self.active = True

    def outside_screen(self):
        return self.x < 0 or self.x > c.screen_width or self.y < 0 or self.y > c.screen_height

    def update(self):
        self.ripple.update()

        if self.ripple.display == False:
            self.active = False

    def render(self):
        self.ripple.render()