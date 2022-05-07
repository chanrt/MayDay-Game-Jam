import pygame as pg

from constants import consts as c
from load_data import get_resource_path

def instructions(screen):
    bg_color = pg.Color(32, 32, 32)

    images = []
    for i in range(1, 11):
        file_string = "instructions/Slide{}.PNG".format(i)
        image = pg.image.load(get_resource_path(file_string))
        images.append(image)

    x_extra = c.screen_width - images[0].get_width()
    y_extra = c.screen_height - images[0].get_height()
    x = x_extra // 2
    y = y_extra // 2

    current_image = 1

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
                if current_image > 1 and (event.key == pg.K_a or event.key == pg.K_LEFT):
                    current_image -= 1
                if current_image < 10 and (event.key == pg.K_d or event.key == pg.K_RIGHT):
                    current_image += 1

        screen.fill(bg_color)
        screen.blit(images[current_image - 1], (x, y))
        pg.display.flip()

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.set_screen_size(screen)
    instructions(screen)