import pygame as pg

from about import about
from constants import consts as c
from game_loop import game_loop
from instructions import instructions
from load_data import get_resource_path
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
    pg.display.set_caption("Particle Menace")
    c.set_screen_size(screen)
    bg_music = pg.mixer.music.load(get_resource_path("music/menu.mp3"))
    pg.mixer.music.play()

    while True:
        user_input = main_menu(screen)

        if user_input == "play":
            pg.mixer.music.fadeout(500)
            game_loop(screen)
        elif user_input == "instructions":
            instructions(screen)
        elif user_input == "about":
            about(screen)
        elif user_input == "exit":
            pg.quit()
            break
    quit() 