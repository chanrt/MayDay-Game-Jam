def player_artifact_collision(player, artifact):
    if player.num_electrons > 0:
        if player.x - 2 * player.radius < artifact.x + artifact.width and player.x + 2 * player.radius > artifact.x:
            if player.y - 2 * player.radius < artifact.y + artifact.height and player.y + 2 * player.radius > artifact.y:
                return 1
    else:
        if player.x - player.radius < artifact.x + artifact.width and player.x + player.radius > artifact.x:
            if player.y - player.radius < artifact.y + artifact.height and player.y + player.radius > artifact.y:
                return 2
    return 0

def projectile_artifact_collision(projectile, artifact):
    if projectile.x < artifact.x + artifact.width and projectile.x > artifact.x:
        if projectile.y < artifact.y + artifact.height and projectile.y > artifact.y:
            return True
    return False