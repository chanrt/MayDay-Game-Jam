import pygame as pg

from ui.button import Button
from constants import consts as c
from load_data import get_resource_path
from ui.text import Text

def pause_screen(screen):
    clock = pg.time.Clock()

    bg_color = pg.Color(32, 32, 32)

    title_font = pg.font.Font(get_resource_path("fonts/Orbitron-Regular.ttf"), 2 * c.title_font_size)
    button_font = pg.font.Font(get_resource_path("fonts/Orbitron-Regular.ttf"), c.button_font_size)

    title_text = Text(c.screen_width // 2, c.screen_height // 3, "Game Paused", screen)
    title_text.set_font(title_font)

    resume_button = Button(2 * c.screen_width // 6, 2 * c.screen_height // 3, c.screen_width // 7, 2 * c.button_font_size, screen, "Resume")
    resume_button.set_font(button_font)
    restart_button = Button(3 * c.screen_width // 6, 2 * c.screen_height // 3, c.screen_width // 7, 2 * c.button_font_size, screen, "Restart")
    restart_button.set_font(button_font)
    quit_button = Button(4 * c.screen_width // 6, 2 * c.screen_height // 3, c.screen_width // 7, 2 * c.button_font_size, screen, "Main Menu")
    quit_button.set_font(button_font)

    while True:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
            if event.type == pg.MOUSEMOTION:
                mouse_pos = pg.mouse.get_pos()
                resume_button.update(mouse_pos)
                restart_button.update(mouse_pos)
                quit_button.update(mouse_pos)
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                click = event.button
                resume_button.check_clicked(mouse_pos, click)
                restart_button.check_clicked(mouse_pos, click)
                quit_button.check_clicked(mouse_pos, click)

                if resume_button.left_clicked:
                    return "resume"
                elif restart_button.left_clicked:
                    return "restart"
                elif quit_button.left_clicked:
                    return "quit"

            if event.type == pg.MOUSEBUTTONUP:
                mouse_pos = pg.mouse.get_pos()
                click = event.button
                resume_button.check_released(mouse_pos, click)
                restart_button.check_released(mouse_pos, click)
                quit_button.check_released(mouse_pos, click)
        
        screen.fill(bg_color)

        title_text.render()
        resume_button.render()
        restart_button.render()
        quit_button.render()

        pg.display.flip()

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.set_screen_size(screen)
    pause_screen(screen)