import pygame as pg

from constants import consts as c
from game_loop import game_loop
from main_menu import main_menu

if __name__ == '__main__':
    try:
        import pyi_splash
        pyi_splash.update_text("Loading game")
        pyi_splash.close()
    except:
        pass

    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.set_screen_size(screen)

    while True:
        user_input = main_menu(screen)

        if user_input == "play":
            game_loop(screen)
        elif user_input == "exit":
            pg.quit()
            break
    quit() 