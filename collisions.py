from constants import consts as c


def player_artifact_collision(player, artifact):
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

def projectile_artifact_collision(projectile, artifact):
    rect = artifact.rect
    if projectile.x < rect.x + rect.width and projectile.x > rect.x:
        if projectile.y < rect.y + rect.height and projectile.y > rect.y:
            return True
    return False

def enemy_artifact_collision(enemy, artifact):
    rect = artifact.rect
    if enemy.x < rect.x + rect.width and enemy.x > rect.x:
        if enemy.y < rect.y + rect.height and enemy.y > rect.y:
            return True
    return False

def player_enemy_collision(player, enemy):
    if distance_between(player, enemy) < player.radius:
        return True
    return False

def enemy_projectile_collision(projectile, enemy):
    if distance_between(projectile, enemy) < c.projectile_radius + enemy.radius:
        return True
    return False

def distance_between(player, enemy):
    return ((player.x - enemy.x) ** 2 + (player.y - enemy.y) ** 2) ** 0.5