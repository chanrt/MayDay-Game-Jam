import pygame as pg

from constants import consts as c
from load_data import get_resource_path

def about(screen):
    bg_color = pg.Color(32, 32, 32)
    image = pg.image.load(get_resource_path("about/Slide1.PNG"))
    x_extra = c.screen_width - image.get_width()
    y_extra = c.screen_height - image.get_height()
    x = x_extra // 2
    y = y_extra // 2

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
        
        screen.fill(bg_color)
        screen.blit(image, (x, y))
        pg.display.flip()

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.set_screen_size(screen)
    about(screen)