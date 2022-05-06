from constants import consts as c


def update_artifacts(artifacts):
    for artifact in artifacts:
            artifact.x -= c.scroll_speed * c.dt

    for artifact in artifacts:
        if artifact.x < -artifact.width:
            artifacts.remove(artifact)