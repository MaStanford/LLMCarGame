import math

def _execute_chase_behavior(enemy, game_state, edata):
    """Moves the enemy towards the player."""
    dx = game_state.car_world_x - enemy.x
    dy = game_state.car_world_y - enemy.y
    dist = math.sqrt(dx*dx + dy*dy)
    if dist > 0:
        enemy.vx = (dx / dist) * edata.speed
        enemy.vy = (dy / dist) * edata.speed

def _execute_strafe_behavior(enemy, game_state, edata):
    """Circles the player at a distance."""
    dx = game_state.car_world_x - enemy.x
    dy = game_state.car_world_y - enemy.y
    # Strafe logic: move perpendicular to the player
    enemy.vx = -dy / (dx**2 + dy**2)**0.5 * edata.speed
    enemy.vy = dx / (dx**2 + dy**2)**0.5 * edata.speed

def _execute_ram_behavior(enemy, game_state, edata):
    """Moves aggressively towards the player."""
    dx = game_state.car_world_x - enemy.x
    dy = game_state.car_world_y - enemy.y
    dist = math.sqrt(dx*dx + dy*dy)
    if dist > 0:
        enemy.vx = (dx / dist) * edata.speed * 1.5 # 50% speed boost
        enemy.vy = (dy / dist) * edata.speed * 1.5

def _execute_evade_behavior(enemy, game_state, edata):
    """Moves away from the player."""
    dx = game_state.car_world_x - enemy.x
    dy = game_state.car_world_y - enemy.y
    dist = math.sqrt(dx*dx + dy*dy)
    if dist > 0:
        enemy.vx = -(dx / dist) * edata.speed
        enemy.vy = -(dy / dist) * edata.speed

def _execute_stationary_behavior(enemy):
    """Stops the enemy's movement."""
    enemy.vx = 0
    enemy.vy = 0
