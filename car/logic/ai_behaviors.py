import math
import random
from ..entities.obstacles.mine import Mine

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
    dist = math.sqrt(dx*dx + dy*dy)
    if dist > 0:
        # Move perpendicular to the player
        enemy.vx = -dy / dist * edata.speed
        enemy.vy = dx / dist * edata.speed

def _execute_ram_behavior(enemy, game_state, edata):
    """Moves aggressively towards the player with a speed boost."""
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

def _execute_stationary_behavior(enemy, game_state, edata):
    """Stops the enemy's movement."""
    enemy.vx = 0
    enemy.vy = 0

def _execute_patrol_behavior(entity, game_state):
    """
    Moves the entity towards its patrol target.
    If the target is reached, a new one is generated.
    """
    if entity.patrol_target_x is None:
        # Assign an initial patrol target if none exists
        entity.patrol_target_x = entity.x + random.uniform(-100, 100)
        entity.patrol_target_y = entity.y + random.uniform(-100, 100)

    # Check if the entity has reached its target
    dist_to_target_sq = (entity.x - entity.patrol_target_x)**2 + (entity.y - entity.patrol_target_y)**2
    if dist_to_target_sq < 25: # Close enough
        entity.patrol_target_x = entity.x + random.uniform(-100, 100)
        entity.patrol_target_y = entity.y + random.uniform(-100, 100)

    # Move towards the target
    angle_to_target = math.atan2(entity.patrol_target_y - entity.y, entity.patrol_target_x - entity.x)
    entity.angle = angle_to_target
    entity.pedal_position = 0.5 # Cruise speed



def _execute_deploy_mine_behavior(entity, game_state):
    """
    Flees from the player and deploys a mine.
    """
    if "mine_cooldown" not in entity.ai_state:
        entity.ai_state["mine_cooldown"] = 0

    if entity.ai_state["mine_cooldown"] > 0:
        entity.ai_state["mine_cooldown"] -= 1
        # While cooling down, just chase the player
        _execute_chase_behavior(entity, game_state)
        return

    # Flee from the player
    angle_from_player = math.atan2(entity.y - game_state.car_world_y, entity.x - game_state.car_world_x)
    entity.angle = angle_from_player
    entity.pedal_position = 1.0

    # Deploy a mine if far enough away
    dist_from_player_sq = (entity.x - game_state.car_world_x)**2 + (entity.y - game_state.car_world_y)**2
    if dist_from_player_sq > 100: # Deploy mine when 10 units away
        from ..entities.obstacles.mine import Mine
        new_mine = Mine(entity.x, entity.y)
        game_state.active_obstacles.append(new_mine)
        entity.ai_state["mine_cooldown"] = 150 # 5 seconds cooldown
