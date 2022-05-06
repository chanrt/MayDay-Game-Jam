from math import atan2
from random import random
from time import time
import pygame as pg

from artifacts import *
from collisions import *
from constants import consts as c
from explosion import Explosion
from load_data import get_resource_path
from player import Player
from projectile import Projectile
from text import Text


def game_loop(screen):
    clock = pg.time.Clock()

    simple_font = pg.font.SysFont("arial", 20)

    # title text
    title_text = Text(c.screen_width // 2, c.title_font_size // 2, "Particle Menace", screen)
    title_font = pg.font.Font(get_resource_path("fonts/Orbitron-Regular.ttf"), c.title_font_size)
    title_text.set_font(title_font)

    # colors
    font_color = pg.Color("white")
    bg_color = pg.Color(32, 32, 32)

    # game objects
    player = Player(6, "normal", screen)

    # artifacts
    artifacts = []

    # projectiles
    projectiles = []

    # animations
    animations = []
    game_over_animation = None

    # game events
    spawn_artifact = pg.USEREVENT + 1
    pg.time.set_timer(spawn_artifact, 1000)

    while True:
        start = time()
        clock.tick(120)

        # check game over
        if game_over_animation is not None:
            if not game_over_animation.display:
                pg.quit()
                quit()

        # clean projectiles
        for projectile in projectiles:
            if projectile.outside_screen():
                projectiles.remove(projectile)

        # handle player input
        keys_pressed = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == spawn_artifact:
                if random() < c.artifact_probability:
                    y = random() * (c.screen_height - c.artifact_height)
                    new_artifact = pg.Rect(c.screen_width, y, c.artifact_width, c.artifact_height)
                    artifacts.append(new_artifact)
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
                if event.key == pg.K_q:
                    player.increase_mass(0.2)
                if event.key == pg.K_e:
                    player.decrease_mass(0.2)

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # new projectile
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    angle_between = atan2(mouse_y - player.y, mouse_x - player.x)
                    new_projectile = Projectile(player.x, player.y, angle_between, player.nucleus_color, screen)
                    projectiles.append(new_projectile)

            if event.type == pg.QUIT:
                pg.quit()
                quit()

        # updates
        player.update(keys_pressed)
        update_artifacts(artifacts)

        for projectile in projectiles:
            projectile.update()
        for animation in animations:
            animation.update()

        # collisions between artifacts and players
        collision_status = -1
        for artifact in artifacts:
            collision_status = player_artifact_collision(player, artifact)
            if collision_status != 0:
                break
        
        if collision_status == 1:
            player.lose_electrons()
        elif collision_status == 2:
            explosion = Explosion(player.x, player.y, player.radius, player.nucleus_color, screen)
            animations.append(explosion)
            game_over_animation = explosion
            player.alive = False

        # collisions between artifacts and projectiles
        for artifact in artifacts:
            for projectile in projectiles:
                if projectile_artifact_collision(projectile, artifact):
                    projectiles.remove(projectile)

        # clear screen
        screen.fill(bg_color)

        # render
        player.render()

        for artifact in artifacts:
            pg.draw.rect(screen, c.artifact_color, artifact)
        for projectile in projectiles:
            projectile.render()
        for animation in animations:
            animation.render()

        title_text.render()

        fps_display = simple_font.render("FPS: " + str(int(clock.get_fps())), True, font_color)
        screen.blit(fps_display, (0, 0))

        # flip display
        pg.display.flip()

        end = time()
        c.set_dt(end - start)

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.set_screen_size(screen)

    game_loop(screen)