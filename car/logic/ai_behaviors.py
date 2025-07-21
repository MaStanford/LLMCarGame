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

def _execute_patrol_behavior(enemy, game_state, edata):
    """Moves the enemy between two patrol points."""
    # Initialize patrol points on the first run
    if not hasattr(enemy, 'patrol_start'):
        enemy.patrol_start = (enemy.x - 10, enemy.y - 10)
        enemy.patrol_end = (enemy.x + 10, enemy.y + 10)
        enemy.patrol_target = enemy.patrol_end

    # Determine target coordinates
    target_x, target_y = enemy.patrol_target

    # Move towards the target
    dx = target_x - enemy.x
    dy = target_y - enemy.y
    dist = math.sqrt(dx*dx + dy*dy)

    if dist > 1: # If not at the target yet
        enemy.vx = (dx / dist) * edata.speed * 0.5 # Patrol at half speed
        enemy.vy = (dy / dist) * edata.speed * 0.5
    else:
        # Arrived at target, switch to the other point
        enemy.patrol_target = enemy.patrol_start if enemy.patrol_target == enemy.patrol_end else enemy.patrol_end
        enemy.vx = 0
        enemy.vy = 0

def _execute_deploy_mine_behavior(enemy, game_state, edata):
    """Stops and lays a mine behind the enemy."""
    # Stop moving to deploy
    enemy.vx = 0
    enemy.vy = 0

    # Use a cooldown to prevent spamming
    if not hasattr(enemy, 'mine_cooldown'):
        enemy.mine_cooldown = 0
    
    if enemy.mine_cooldown <= 0:
        # Get position behind the enemy
        # (This is a simplified model, assuming enemy is facing player)
        dx = game_state.car_world_x - enemy.x
        dy = game_state.car_world_y - enemy.y
        dist = math.sqrt(dx*dx + dy*dy)
        
        mine_x = enemy.x - (dx / dist) * 2 # Place it 2 units behind
        mine_y = enemy.y - (dy / dist) * 2

        game_state.active_obstacles.append(Mine(mine_x, mine_y))
        enemy.mine_cooldown = 5 * 30 # 5-second cooldown at 30 FPS
    else:
        enemy.mine_cooldown -= 1
