from anims.ripple import Ripple

class RippleGenerator:
    def __init__(self, x, y, start_radius, end_radius, gen_radius, speed, color, screen):
        self.x = x
        self.y = y
        self.start_radius = start_radius
        self.end_radius = end_radius
        self.gen_radius = gen_radius
        self.speed = speed
        self.color = color
        self.screen = screen

        self.display = True
        self.ripples = []
        self.add_ripple()

    def add_ripple(self):
        first_ripple = Ripple(self.x, self.y, self.start_radius, self.end_radius, self.color, self.screen)
        first_ripple.speed = self.speed
        self.ripples.append(first_ripple)

    def clear_ripples(self):
        self.ripples = []

    def move(self, x, y):
        self.x = x
        self.y = y

        for ripple in self.ripples:
            ripple.x = x
            ripple.y = y

    def update(self):
        for ripple in self.ripples:
            ripple.update()

        if len(self.ripples) > 0:
            recent_ripple = self.ripples[-1]
            if recent_ripple.inwards:
                if recent_ripple.radius < self.gen_radius:
                    new_ripple = Ripple(self.x, self.y, self.start_radius, self.end_radius, self.color, self.screen)
                    new_ripple.speed = self.speed
                    self.ripples.append(new_ripple)
            else:
                if recent_ripple.radius > self.gen_radius:
                    new_ripple = Ripple(self.x, self.y, self.start_radius, self.end_radius, self.color, self.screen)
                    new_ripple.speed = self.speed
                    self.ripples.append(new_ripple)

            for ripple in self.ripples:
                if ripple.display == False:
                    self.ripples.remove(ripple)
        elif len(self.ripples) == 0 and self.display:
            self.add_ripple()

    def render(self):
        if self.display:
            for ripple in self.ripples:
                ripple.render()