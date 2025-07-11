import math
import random

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
    """Moves the enemy back and forth along a patrol path."""
    # Initialize patrol direction if not present
    if not hasattr(enemy, 'patrol_direction'):
        enemy.patrol_direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    
    # Check if it's time to change direction (e.g., after a certain time)
    if not hasattr(enemy, 'patrol_timer'):
        enemy.patrol_timer = 5 # seconds
    
    # In a real implementation, you'd decrement this timer
    # For now, we'll just keep the movement simple.
    
    enemy.vx = enemy.patrol_direction[0] * edata.speed * 0.5 # Patrol at half speed
    enemy.vy = enemy.patrol_direction[1] * edata.speed * 0.5

def _execute_deploy_mine_behavior(enemy, game_state, edata):
    """Stops and attempts to lay a mine behind it."""
    # Stop moving to deploy
    enemy.vx = 0
    enemy.vy = 0
    # In the main game loop, you would check for this behavior
    # and trigger the mine-laying logic.
    # e.g., world.add_obstacle(Mine(enemy.x, enemy.y))
    # This function itself just handles the movement part.
    # We can add a cooldown to prevent constant mine laying.
    if not hasattr(enemy, 'mine_cooldown') or enemy.mine_cooldown <= 0:
        # Signal to the game world that a mine should be dropped
        # This is a conceptual implementation. The actual creation
        # of the mine object would happen in the world update logic.
        game_state.request_mine_deployment(enemy.x, enemy.y)
        enemy.mine_cooldown = 5 # 5-second cooldown
