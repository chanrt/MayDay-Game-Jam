from itertools import product
from math import atan2
from random import random
import pygame as pg

from objs.artifacts import Artifact
from objs.burst import Burst
from collisions import *
from constants import consts as c
from anims.directed_explosion import DirectedExplosion
from objs.enemy import Enemy
from anims.explosion import Explosion
from anims.fade import Fade
from powerups.higgs_field import HiggsField
from load_data import get_resource_path
from pause_screen import pause_screen
from objs.player import Player
from ui.progress_bar import ProgressBar
from objs.projectile import Projectile
from objs.portal import Portal
from ui.text import Text


def game_loop(screen, matter="anti"):
    clock = pg.time.Clock()

    # states
    current_matter = matter
    opposite_matter = "anti" if matter == "normal" else "normal"

    # colors
    font_color = pg.Color("white")
    bg_color = pg.Color(32, 32, 32)
    dominant_color = c.normal_nucleus_color if current_matter == "normal" else c.anti_nucleus_color

    # game objects
    player = Player(13.2, current_matter, screen)

    # fonts
    simple_font = pg.font.SysFont("arial", 20)
    title_font = pg.font.Font(get_resource_path("fonts/Orbitron-Regular.ttf"), c.title_font_size)
    indicator_font = pg.font.Font(get_resource_path("fonts/Orbitron-Regular.ttf"), c.indicator_font_size)

    # text
    title_text = Text(c.screen_width // 2, c.title_font_size // 2, "Particle Menace", screen)
    title_text.set_font(title_font)
    below_title = c.title_font_size + c.indicator_font_size // 2
    mass_text = Text(c.screen_width // 4, below_title, "Mass", screen)
    mass_text.set_font(indicator_font)
    energy_text = Text(3 * c.screen_width // 4, below_title, "Energy", screen)
    energy_text.set_font(indicator_font)
    remaining_distance_text = Text(c.screen_width // 2, c.screen_height - c.title_font_size, "Distance to portal:", screen)
    remaining_distance_text.set_font(title_font)

    # progress bars
    below_indicator = c.title_font_size + c.indicator_font_size + 2 * c.progress_bar_thickness
    mass_bar = ProgressBar(c.screen_width // 4, below_indicator, c.screen_width // 4, c.progress_bar_thickness, screen)
    mass_bar.fg_color = dominant_color
    mass_bar.set_progress(player.mass / c.max_mass)
    energy_bar = ProgressBar(3 * c.screen_width // 4, below_indicator, c.screen_width // 4, c.progress_bar_thickness, screen)
    energy_bar.set_progress(player.energy / c.max_energy)
    energy_bar.fg_color = dominant_color

    # music
    pg.mixer.music.load(get_resource_path("music/game.mp3"))
    pg.mixer.music.play(-1)

    # sounds
    artifact_enemy_collision_sound = pg.mixer.Sound(get_resource_path("sounds/artifact_enemy_collision.wav"))
    burst_sound = pg.mixer.Sound(get_resource_path("sounds/burst.wav"))
    enemy_player_collision_sound = pg.mixer.Sound(get_resource_path("sounds/enemy_player_collision.wav"))
    enemy_hit_sound = pg.mixer.Sound(get_resource_path("sounds/enemy_hit.wav"))
    enemy_death_sound = pg.mixer.Sound(get_resource_path("sounds/enemy_death.wav"))
    enemy_shoot_sound = pg.mixer.Sound(get_resource_path("sounds/enemy_shoot.wav"))
    enemy_shoot_sound.set_volume(0.1)
    energy_from_mass_sound = pg.mixer.Sound(get_resource_path("sounds/energy_from_mass.wav"))
    energy_from_mass_sound.set_volume(0.3)
    higgs_sound = pg.mixer.Sound(get_resource_path("sounds/higgs.wav"))
    matter_change_sound = pg.mixer.Sound(get_resource_path("sounds/matter_change.wav"))
    player_shoot_sound = pg.mixer.Sound(get_resource_path("sounds/player_shoot.wav"))
    player_shoot_sound.set_volume(0.15)
    player_death_sound = pg.mixer.Sound(get_resource_path("sounds/player_death.wav"))
    player_hit_sound = pg.mixer.Sound(get_resource_path("sounds/player_hit.wav"))
    player_mass_absorb_sound = pg.mixer.Sound(get_resource_path("sounds/player_mass_absorb.wav"))
    player_mass_absorb_sound.set_volume(0.2)
    ricochet_sound = pg.mixer.Sound(get_resource_path("sounds/ricochet.wav"))
    ricochet_sound.set_volume(0.5)
    portal_sound = pg.mixer.Sound(get_resource_path("sounds/teleport.wav"))

    # animations
    animations = []
    game_over_animation = None
    end_portal = None

    # artifacts
    artifacts = []

    # bursts
    bursts = []

    # enemies
    enemies = []

    # powerups
    powerups = []

    # projectiles
    projectiles = []

    # game events
    spawn_artifact = pg.USEREVENT + 1
    pg.time.set_timer(spawn_artifact, 1000)
    spawn_enemy = pg.USEREVENT + 2
    pg.time.set_timer(spawn_enemy, 1500)

    paused = 0
    portal_reached = False
    fire_button_pressed = False
    game_time = 0

    while True:
        clock.tick(120)

        # garbage collection
        for animation in animations:
            if not animation.display:
                animations.remove(animation)
                if isinstance(animation, DirectedExplosion):
                    # absorbing mass
                    player.increase_mass(c.mass_absorption * animation.source.init_mass)
                    player_mass_absorb_sound.play()
        for burst in bursts:
            if burst.outside_screen() or burst.active == False:
                bursts.remove(burst)
        for artifact in artifacts:
            if artifact.outside_screen():
                artifacts.remove(artifact)
        for enemy in enemies:
            if enemy.outside_screen():
                enemies.remove(enemy)
        for projectile in projectiles:
            if projectile.outside_screen() or projectile.active == False:
                projectiles.remove(projectile)       

        # handle player input
        keys_pressed = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == spawn_artifact and c.max_time - game_time > 5:
                if random() < c.artifact_probability:
                    # generate artifact
                    y = random() * (c.screen_height - c.artifact_height)
                    new_artifact = Artifact(y, screen)
                    artifacts.append(new_artifact)

            if event.type == spawn_enemy:
                if random() < c.enemy_probability and c.max_time - game_time > 5:
                    # generate enemy
                    y = random() * (c.screen_height)
                    mass = c.min_enemy_mass + random() * (c.max_enemy_mass - c.min_enemy_mass)
                    new_enemy = Enemy(y, mass, opposite_matter, screen)
                    enemies.append(new_enemy)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    c.pause_menu_sound.play()
                    paused = 2
                    user_input = pause_screen(screen)
                    if user_input != "resume":
                        animations = []
                        artifacts = []
                        enemies = []
                        projectiles = []
                    if user_input == "quit":
                        return
                    elif user_input == "restart":
                        game_loop(screen)
                        return

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    fire_button_pressed = True
                if player.matter == "anti" and event.button == 3:
                    if player.mass > c.burst_mass:
                        burst_sound.play()
                        new_burst = Burst(player.x, player.y, dominant_color, screen)
                        bursts.append(new_burst)
                        player.decrease_mass(c.burst_mass)

            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    fire_button_pressed = False
                    
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        # update UI
        mass_bar.set_progress(player.mass / c.max_mass)
        energy_bar.set_progress(player.energy / c.max_energy)
        remaining_distance_text.set_text(f"Distance to portal: {int(c.max_time - game_time)} light years")
        c.scroll_speed = c.min_scroll_speed + (c.max_scroll_speed - c.min_scroll_speed) * game_time / c.max_time

        # fire projectiles (player)
        if fire_button_pressed and player.fire_cycle <= 0:
            player_shoot_sound.play()
            mouse_x, mouse_y = pg.mouse.get_pos()
            angle = atan2(mouse_y - player.y, mouse_x - player.x)
            new_projectile = Projectile(player.x, player.y, angle, player.nucleus_color, False, screen)
            projectiles.append(new_projectile)
            player.decrease_energy(c.energy_per_shot)
            player.fire_cycle = c.player_fire_cooldown

            if player.converting_mass_to_energy and player.convert_energy_cycle == 0:
                energy_from_mass_sound.play()

        # updates
        if not paused and not portal_reached:
            player.update(keys_pressed, c.dt * 1000)
            for animation in animations:
                animation.update()
            for artifact in artifacts:
                artifact.update()
            for burst in bursts:
                burst.update()
            for enemy in enemies:
                enemy.update(player, artifacts, c.dt * 1000)
            for powerup in powerups:
                powerup.update()
            for projectile in projectiles:
                projectile.update()
            if end_portal is not None:
                end_portal.update()
                if player.x > end_portal.x:
                    portal_reached = True
                    fade = Fade(0, 255, 120, c.fade_out_color, screen)
                    animations.append(fade)
                    game_over_animation = fade
                    pg.mixer.music.stop()
                    portal_sound.play()

        if portal_reached:
            game_over_animation.update()

        # see if any enemy is ready to fire
        for enemy in enemies:
            if enemy.fire_cycle <= 0:
                enemy_shoot_sound.play()
                angle = atan2(player.y - enemy.y, player.x - enemy.x)
                new_projectile = Projectile(enemy.x, enemy.y, angle, enemy.color, True, screen)
                projectiles.append(new_projectile)
                enemy.fire_cycle = c.enemy_fire_cooldown

        # collisions between artifacts and enemies
        for artifact in artifacts:
            for enemy in enemies:
                if artifact_enemy_collision(artifact, enemy):
                    artifact_enemy_collision_sound.play()
                    explosion = Explosion(enemy.x, enemy.y, enemy.radius,
                                          enemy.color, screen)
                    animations.append(explosion)
                    enemies.remove(enemy)

        # collisions between artifacts and players
        if player.alive:
            collision_status = -1
            for artifact in artifacts:
                collision_status = artifact_player_collision(artifact, player)
                if collision_status != 0:
                    break
            if collision_status == 1:
                player.lose_electrons()
                mass_bar.set_progress(player.mass / c.max_mass)
            elif collision_status == 2:
                explosion = Explosion(player.x, player.y, player.radius, player.nucleus_color, screen)
                animations.append(explosion)
                game_over_animation = explosion
                player_death_sound.play()
                player.alive = False

        # collisions between artifacts and projectiles
        for artifact in artifacts:
            for projectile in projectiles:
                if artifact_projectile_collision(artifact, projectile):
                    ricochet_sound.play()
                    projectiles.remove(projectile)

        # collisions between burst and enemies
        for burst in bursts:
            for enemy in enemies:
                if burst_enemy_collision(burst, enemy):
                    enemies.remove(enemy)
                    enemy_death_sound.play()
                    if player.num_electrons > 0:
                        explosion = Explosion(enemy.x, enemy.y, enemy.radius, enemy.color, screen)
                        animations.append(explosion)
                    else:
                        directed_explosion = DirectedExplosion(enemy, player, enemy.radius, enemy.color, screen)
                        animations.append(directed_explosion)

        # collisions between burst and projectiles
        for burst in bursts:
            for projectile in projectiles:
                if burst.color != projectile.color and burst_projectile_collision(burst, projectile):
                    projectiles.remove(projectile)
                    explosion = Explosion(projectile1.x, projectile1.y, 2 * c.projectile_radius, c.annihilation_color, screen)
                    explosion.final_step = 50
                    animations.append(explosion)

        # collisions between enemies and player
        if player.alive:
            for enemy in enemies:
                if enemy_player_collision(enemy, player):
                    enemy_player_collision_sound.play()
                    enemies.remove(enemy)
                    explosion = Explosion(enemy.x, enemy.y, enemy.radius, enemy.color, screen)
                    animations.append(explosion)

                    player.decrease_mass((1 + c.collision_collateral) * enemy.mass)
                    mass_bar.set_progress(player.mass / c.max_mass)
                    if player.alive == False:
                        player_death_sound.play()
                        explosion = Explosion(player.x, player.y, player.radius, player.nucleus_color, screen)
                        animations.append(explosion)
                        game_over_animation = explosion

        # collisions between enemies and projectiles
        for enemy in enemies:
            for projectile in projectiles:
                if projectile.color != enemy.color and enemy_projectile_collision(enemy, projectile):
                    enemy_hit_sound.play()
                    enemy.take_damage(c.damage_to_enemy)
                    projectiles.remove(projectile)
        
        # collisions between player and powerups
        if player.alive:
            for powerup in powerups:
                if player_powerup_collision(player, powerup):
                    powerups.remove(powerup)
                    if isinstance(powerup, HiggsField):
                        higgs_sound.play()
                        player.increase_mass(c.higgs_mass_gain)

        # collisions between player and projectiles
        if player.alive:
            for projectile in projectiles:
                if projectile.color != player.nucleus_color and player_projectile_collision(player, projectile):
                    player_hit_sound.play()
                    player.decrease_mass(c.damage_to_player)
                    projectiles.remove(projectile)
                    mass_bar.set_progress(player.mass / c.max_mass)
                    if player.alive == False:
                            player_death_sound.play()
                            explosion = Explosion(player.x, player.y, player.radius, player.nucleus_color, screen)
                            animations.append(explosion)
                            game_over_animation = explosion

        # collisions between projectiles
        for projectile1, projectile2 in product(projectiles, projectiles):
            if projectile1 != projectile2 and projectile_projectile_collision(projectile1, projectile2):
                projectile1.active = False
                projectile2.active = False
                explosion = Explosion(projectile1.x, projectile1.y, 2 * c.projectile_radius, c.annihilation_color, screen)
                explosion.final_step = 50
                animations.append(explosion)

        # remove dead enemies and consider spawning powerups/pickups
        for enemy in enemies:
            if enemy.alive == False:
                enemy_death_sound.play()
                if player.num_electrons > 0:
                    explosion = Explosion(enemy.x, enemy.y, enemy.radius, enemy.color, screen)
                    animations.append(explosion)
                else:
                    directed_explosion = DirectedExplosion(enemy, player, enemy.radius, enemy.color, screen)
                    animations.append(directed_explosion)
                enemies.remove(enemy)

                if player.mass < c.higgs_mass_cutoff and random() < c.higgs_probability:
                    higgs_field = HiggsField(enemy.x, enemy.y, screen)
                    powerups.append(higgs_field)

        # check game over
        if game_over_animation is not None:
            if not game_over_animation.display:
                if isinstance(game_over_animation, Explosion):
                    # player death
                    game_over_animation = None
                    matter_change_sound.play()

                    current_matter = "anti" if current_matter == "normal" else "normal"
                    opposite_matter = "anti" if opposite_matter == "normal" else "normal"
                    dominant_color = c.normal_nucleus_color if current_matter == "normal" else c.anti_nucleus_color

                    player.change_matter()
                    player.reset_position()

                    for artifact in artifacts:
                        if abs(artifact.x - player.x) < c.screen_width // 2:
                            artifacts.remove(artifact)

                    for enemy in enemies:
                        enemy.change_matter()
                    for projectile in projectiles:
                        projectile.change_matter()
                    mass_bar.fg_color = dominant_color
                    energy_bar.fg_color = dominant_color
                elif isinstance(game_over_animation, Fade):
                    # game finished
                    game_over_animation = None
                    pg.mixer.music.load(get_resource_path("music/menu.mp3"))
                    pg.mixer.music.play()
                    return

        # check if portal can be generated
        if end_portal is None and c.max_time - game_time < 2:
            end_portal = Portal(dominant_color, screen) 

        # clear screen
        screen.fill(bg_color)

        # render
        player.render()
        for animation in animations:
            animation.render()
        for artifact in artifacts:
            artifact.render()
        for burst in bursts:
            burst.render()
        for enemy in enemies:
            enemy.render()
        for powerup in powerups:
            powerup.render()
        for projectile in projectiles:
            projectile.render()
        if end_portal is not None:
            end_portal.render()

        energy_text.render()
        title_text.render()
        mass_text.render()
        remaining_distance_text.render()
        
        energy_bar.render()
        mass_bar.render()

        fps_string = "FPS: " + str(int(clock.get_fps()))
        fps_display = simple_font.render(fps_string, True, font_color)
        screen.blit(fps_display, (0, 0))

        # flip display
        pg.display.flip()

        if not paused:
            c.set_dt(clock.get_time() / 1000)
        else:
            paused -= 1
            c.set_dt(0)

        if not portal_reached:
            game_time += c.dt
        else:
            game_time = c.max_time

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.set_screen_size(screen)

    game_loop(screen)