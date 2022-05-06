from math import atan2
from random import random
import pygame as pg

from artifacts import Artifact
from collisions import *
from constants import consts as c
from enemy import Enemy
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

    # sounds
    player_shoot_sound = pg.mixer.Sound(get_resource_path("sounds/player_shoot.wav"))
    player_shoot_sound.set_volume(0.2)
    player_death_sound = pg.mixer.Sound(get_resource_path("sounds/player_death.wav"))
    ricochet_sound = pg.mixer.Sound(get_resource_path("sounds/ricochet.wav"))
    artifact_enemy_collision_sound = pg.mixer.Sound(get_resource_path("sounds/artifact_enemy_collision.wav"))
    enemy_player_collision_sound = pg.mixer.Sound(get_resource_path("sounds/enemy_player_collision.wav"))
    enemy_hit_sound = pg.mixer.Sound(get_resource_path("sounds/enemy_hit.wav"))
    enemy_death_sound = pg.mixer.Sound(get_resource_path("sounds/enemy_death.wav"))

    # colorsd
    font_color = pg.Color("white")
    bg_color = pg.Color(32, 32, 32)

    # states
    current_matter = "normal"
    opposite_matter = "anti"

    # game objects
    player = Player(6, current_matter, screen)

    # artifacts
    artifacts = []

    # projectiles
    projectiles = []

    # enemies
    enemies = []

    # animations
    animations = []
    game_over_animation = None

    # game events
    spawn_artifact = pg.USEREVENT + 1
    pg.time.set_timer(spawn_artifact, 1000)
    spawn_enemy = pg.USEREVENT + 2
    pg.time.set_timer(spawn_enemy, 1500)

    while True:
        clock.tick(120)

        # check game over
        if game_over_animation is not None:
            if not game_over_animation.display:
                pg.quit()
                quit()

        # clean artifacts
        for artifact in artifacts:
            if artifact.outside_screen():
                artifacts.remove(artifact)

        # clear animations
        for animation in animations:
            if not animation.display:
                animations.remove(animation)

        # clean enemies
        for enemy in enemies:
            if enemy.outside_screen():
                enemies.remove(enemy)

        # clean projectiles
        for projectile in projectiles:
            if projectile.outside_screen():
                projectiles.remove(projectile)        

        # handle player input
        keys_pressed = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == spawn_artifact:
                if random() < c.artifact_probability:
                    # generate artifact
                    y = random() * (c.screen_height - c.artifact_height)
                    new_artifact = Artifact(y, screen)
                    artifacts.append(new_artifact)

            if event.type == spawn_enemy:
                if random() < c.enemy_probability:
                    # generate enemy
                    y = random() * (c.screen_height)
                    mass = 0.5 * random() * player.mass
                    new_enemy = Enemy(y, mass, opposite_matter, screen)
                    enemies.append(new_enemy)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
                if event.key == pg.K_q:
                    # CHEAT
                    player.increase_mass(0.2)
                if event.key == pg.K_e:
                    # CHEAT
                    player.decrease_mass(0.2)

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # new projectile
                    player_shoot_sound.play()
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    angle = atan2(mouse_y - player.y, mouse_x - player.x)
                    new_projectile = Projectile(player.x, player.y, angle, player.nucleus_color, screen)
                    projectiles.append(new_projectile)

            if event.type == pg.QUIT:
                pg.quit()
                quit()

        # updates
        player.update(keys_pressed)

        for artifact in artifacts:
            artifact.update()
        for enemy in enemies:
            enemy.update(player, artifacts)
        for projectile in projectiles:
            projectile.update()
        for animation in animations:
            animation.update()

        # collisions between artifacts and players
        if player.alive:
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
                player_death_sound.play()
                player.alive = False

        # collisions between artifacts and projectiles
        for artifact in artifacts:
            for projectile in projectiles:
                if projectile_artifact_collision(projectile, artifact):
                    ricochet_sound.play()
                    projectiles.remove(projectile)

        # collisions between artifacts and enemies
        for artifact in artifacts:
            for enemy in enemies:
                if enemy_artifact_collision(enemy, artifact):
                    artifact_enemy_collision_sound.play()
                    explosion = Explosion(enemy.x, enemy.y, enemy.radius,
                                          enemy.color, screen)
                    animations.append(explosion)
                    enemies.remove(enemy)

        # collisions between player and enemies
        if player.alive:
            for enemy in enemies:
                if player_enemy_collision(player, enemy):
                    enemy_player_collision_sound.play()
                    enemies.remove(enemy)
                    explosion = Explosion(enemy.x, enemy.y, enemy.radius, enemy.color, screen)
                    animations.append(explosion)

        # collisions between enemies and projectiles
        for enemy in enemies:
            for projectile in projectiles:
                if enemy_projectile_collision(projectile, enemy):
                    enemy_hit_sound.play()
                    enemy.take_damage(c.damage_to_enemy)
                    projectiles.remove(projectile)

        for enemy in enemies:
            if enemy.alive == False:
                enemy_death_sound.play()
                explosion = Explosion(enemy.x, enemy.y, enemy.radius, enemy.color, screen)
                animations.append(explosion)
                enemies.remove(enemy)

        # clear screen
        screen.fill(bg_color)

        # render
        player.render()

        for artifact in artifacts:
            artifact.render()
        for enemy in enemies:
            enemy.render()
        for projectile in projectiles:
            projectile.render()
        for animation in animations:
            animation.render()

        title_text.render()

        fps_string = "FPS: " + str(int(clock.get_fps()))
        fps_display = simple_font.render(fps_string, True, font_color)
        screen.blit(fps_display, (0, 0))

        # flip display
        pg.display.flip()

        c.set_dt(clock.get_time() / 1000)


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.set_screen_size(screen)

    game_loop(screen)