from constants import consts as c
from anims.ripple_generator import RippleGenerator

class Portal:
    def __init__(self, color, screen):
        self.x = c.screen_width
        self.y = c.screen_height // 2
        self.color = color
        self.screen = screen

        self.ripple_generator = RippleGenerator(self.x, self.y, 0.1 * c.screen_height, 0.9 * c.screen_width, 0.2 * c.screen_width, 1500, color, screen)

    def update(self):
        self.x -= c.scroll_speed * c.dt
        self.ripple_generator.move(self.x, self.y)
        self.ripple_generator.update()

    def render(self):
        self.ripple_generator.render()