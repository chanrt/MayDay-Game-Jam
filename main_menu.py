from itertools import product
from math import radians
import pygame as pg

from button import Button
from collisions import projectile_projectile_collision
from constants import consts as c
from explosion import Explosion
from load_data import get_resource_path
from projectile import Projectile
from random import randint, random
from text import Text

def make_new_projectiles(screen):
    panel = randint(0, 3)
    color = c.normal_nucleus_color if random() < 0.5 else c.anti_nucleus_color

    if panel == 0:
        x = randint(0, c.screen_width)
        y = 0
        theta = radians(randint(225 + 180, 335 + 180))
        return Projectile(x, y, theta, color, screen)
    elif panel == 1:
        x = c.screen_width
        y = randint(0, c.screen_height)
        theta = radians(randint(135 + 180, 225 + 180))
        return Projectile(x, y, theta, color, screen)
    elif panel == 2:
        x = randint(0, c.screen_width)
        y = c.screen_height
        theta = radians(randint(45 + 180, 135 + 180))
        return Projectile(x, y, theta, color, screen)
    elif panel == 3:
        x = 0
        y = randint(0, c.screen_height)
        theta = radians(randint(225 + 180, 315 + 180))
        return Projectile(x, y, theta, color, screen)


def main_menu(screen):
    clock = pg.time.Clock()

    bg_color = pg.Color(32, 32, 32)
    
    # fonts
    title_font = pg.font.Font(get_resource_path("fonts/Orbitron-Regular.ttf"), 2 * c.title_font_size)
    button_font = pg.font.Font(get_resource_path("fonts/Orbitron-Regular.ttf"), c.button_font_size)

    # title
    title_text = Text(c.screen_width // 2, 2 * c.screen_height // 7, "Particle Menace", screen)
    title_text.set_font(title_font)

    # buttons
    play_button = Button(3 * c.screen_width // 8, 4 * c.screen_height // 7, c.button_width, c.button_height, screen, "Play")
    play_button.set_font(button_font)
    instruction_button = Button(5 * c.screen_width // 8, 4 * c.screen_height // 7, c.button_width, c.button_height, screen, "Instructions")
    instruction_button.set_font(button_font)
    about_button = Button(3 * c.screen_width // 8, 5 * c.screen_height // 7, c.button_width, c.button_height, screen, "About")
    about_button.set_font(button_font)
    exit_button = Button(5 * c.screen_width // 8, 5 * c.screen_height // 7, c.button_width, c.button_height, screen, "Exit")
    exit_button.set_font(button_font)

    num_projectiles = 20
    projectiles = []
    animations = []

    for _ in range(num_projectiles):
        x = randint(0, c.screen_width)
        y = randint(0, c.screen_height)
        theta = radians(randint(0, 360))
        color = c.normal_nucleus_color if random() < 0.5 else c.anti_nucleus_color
        projectiles.append(Projectile(x, y, theta, color, screen))

    while True:
        clock.tick(60)

        for animation in animations:
            if animation.display == False:
                animations.remove(animation)

        for projectile in projectiles:
            if projectile.outside_screen() or projectile.active == False:
                projectiles.remove(projectile)
                projectiles.append(make_new_projectiles(screen))

        while len(projectiles) < num_projectiles:
            projectiles.append(make_new_projectiles(screen))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
            if event.type == pg.MOUSEMOTION:
                mouse_pos = pg.mouse.get_pos()
                play_button.update(mouse_pos)
                instruction_button.update(mouse_pos)
                about_button.update(mouse_pos)
                exit_button.update(mouse_pos)
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                click = event.button
                play_button.check_clicked(mouse_pos, click)
                instruction_button.check_clicked(mouse_pos, click)
                about_button.check_clicked(mouse_pos, click)
                exit_button.check_clicked(mouse_pos, click)

                if play_button.left_clicked:
                    return "play"
                elif instruction_button.left_clicked:
                    return "instructions"
                elif about_button.left_clicked:
                    return "about"
                elif exit_button.left_clicked:
                    return "exit"
            if event.type == pg.MOUSEBUTTONUP:
                mouse_pos = pg.mouse.get_pos()
                click = event.button
                play_button.check_released(mouse_pos, click)
                instruction_button.check_released(mouse_pos, click)
                about_button.check_released(mouse_pos, click)
                exit_button.check_released(mouse_pos, click)
        
        screen.fill(bg_color)

        for projectile in projectiles:
            projectile.update()

        for animation in animations:
            animation.update()

        for projectile1, projectile2 in product(projectiles, projectiles):
            if projectile1 != projectile2 and projectile_projectile_collision(projectile1, projectile2):
                projectile1.active = False
                projectile2.active = False
                explosion = Explosion(projectile1.x, projectile1.y, 2 * c.projectile_radius, c.annihilation_color, screen)
                explosion.final_step = 25
                animations.append(explosion)

        for projectile in projectiles:
            projectile.render()

        for animation in animations:
            animation.render()

        title_text.render()
        play_button.render()
        instruction_button.render()
        about_button.render()
        exit_button.render()

        pg.display.flip()

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.set_screen_size(screen)

    main_menu(screen)