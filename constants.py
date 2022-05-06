class Constants:
    def __init__(self):
        pass

    def set_screen_size(self, screen):
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen.get_size()

consts = Constants()