from player import Player

from constants import consts as c
import pygame as pg

def check_rect_collision(player, rect):
    if player.num_electrons > 0:
        if player.x - 2 * player.radius < rect.x + rect.width and player.x + 2 * player.radius > rect.x:
            if player.y - 2 * player.radius < rect.y + rect.height and player.y + 2 * player.radius > rect.y:
                return 1
    else:
        if player.x - player.radius < rect.x + rect.width and player.x + player.radius > rect.x:
            if player.y - player.radius < rect.y + rect.height and player.y + player.radius > rect.y:
                return 2
    return 0

def game_loop(screen):
    clock = pg.time.Clock()

    bg_color = pg.Color(32, 32, 32)
    rect_color = pg.Color("red")

    rects = []

    player = Player(6, screen)

    while True:
        clock.tick(60)

        collision_status = -1
        for rect in rects:
            collision_status = check_rect_collision(player, rect)
            if collision_status != 0:
                break
        
        if collision_status == 1:
            player.lose_electrons()
        elif collision_status == 2:
            pg.quit()
            quit()

        keys_pressed = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
                if event.key == pg.K_q:
                    player.increase_mass(0.2)
                if event.key == pg.K_e:
                    player.decrease_mass(0.2)

        player.update(keys_pressed)

        screen.fill(bg_color)

        player.render()

        for rect in rects:
            pg.draw.rect(screen, rect_color, rect)

        pg.display.flip()

        print(clock.get_fps())

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.set_screen_size(screen)

    game_loop(screen)