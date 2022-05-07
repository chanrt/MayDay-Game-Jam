from constants import consts as c


def artifact_player_collision(artifact, player):
    rect = artifact.rect
    if player.num_electrons > 0:
        if player.x - 2 * player.radius < rect.x + rect.width and player.x + 2 * player.radius > rect.x:
            if player.y - 2 * player.radius < rect.y + rect.height and player.y + 2 * player.radius > rect.y:
                return 1
    else:
        if player.x - player.radius < rect.x + rect.width and player.x + player.radius > rect.x:
            if player.y - player.radius < rect.y + rect.height and player.y + player.radius > rect.y:
                return 2
    return 0

def artifact_projectile_collision(artifact, projectile):
    rect = artifact.rect
    if projectile.x < rect.x + rect.width and projectile.x > rect.x:
        if projectile.y < rect.y + rect.height and projectile.y > rect.y:
            return True
    return False

def artifact_enemy_collision(artifact, enemy):
    rect = artifact.rect
    if enemy.x < rect.x + rect.width and enemy.x > rect.x:
        if enemy.y < rect.y + rect.height and enemy.y > rect.y:
            return True
    return False

def enemy_player_collision(enemy, player):
    if distance_between(player, enemy) < player.radius:
        return True
    return False

def enemy_powerup_collision(enemy, powerup):
    if distance_between(enemy, powerup) < enemy.radius + powerup.radius:
        return True
    return False

def enemy_projectile_collision(enemy, projectile):
    if distance_between(projectile, enemy) < c.projectile_radius + enemy.radius:
        return True
    return False

def player_powerup_collision(player, powerup):
    if distance_between(player, powerup) < player.radius + powerup.radius:
        return True
    return False

def player_projectile_collision(player, projectile):
    if distance_between(player, projectile) < player.radius + c.projectile_radius:
        return True
    return False

def projectile_projectile_collision(projectile1, projectile2):
    if distance_between(projectile1, projectile2) < 2 * c.projectile_radius:
        return True
    return False

def distance_between(player, enemy):
    return ((player.x - enemy.x) ** 2 + (player.y - enemy.y) ** 2) ** 0.5