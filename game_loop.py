import pygame as pg

def game_loop(screen):

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()

        screen.fill((0, 0, 0))
        pg.display.flip()
            