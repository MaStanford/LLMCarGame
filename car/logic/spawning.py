import random
import math
from .entity_loader import ENEMY_VEHICLES, ENEMY_CHARACTERS, FAUNA, OBSTACLES

def spawn_enemy(game_state, world):
    """Spawns a new enemy."""
    enemy_class = random.choice(ENEMY_VEHICLES + ENEMY_CHARACTERS)
    
    # Find a valid spawn location
    for _ in range(10):
        sangle = random.uniform(0, 2 * math.pi)
        sdist = random.uniform(game_state.spawn_radius * 0.8, game_state.spawn_radius)
        sx = game_state.car_world_x + sdist * math.cos(sangle)
        sy = game_state.car_world_y + sdist * math.sin(sangle)
        
        if world.get_terrain_at(sx, sy).get("passable", True):
            new_enemy = enemy_class(sx, sy)
            game_state.active_enemies.append(new_enemy)
            return

def spawn_fauna(game_state, world):
    """Spawns a new fauna."""
    fauna_class = random.choice(FAUNA)
    
    # Find a valid spawn location
    for _ in range(10):
        sangle = random.uniform(0, 2 * math.pi)
        sdist = random.uniform(game_state.spawn_radius * 0.8, game_state.spawn_radius)
        sx = game_state.car_world_x + sdist * math.cos(sangle)
        sy = game_state.car_world_y + sdist * math.sin(sangle)
        
        if world.get_terrain_at(sx, sy).get("passable", True):
            new_fauna = fauna_class(sx, sy)
            game_state.active_fauna.append(new_fauna)
            return

def spawn_obstacle(game_state, world):
    """Spawns a new obstacle."""
    obstacle_class = random.choice(OBSTACLES)
    
    # Find a valid spawn location
    for _ in range(10):
        sangle = random.uniform(0, 2 * math.pi)
        sdist = random.uniform(game_state.spawn_radius * 0.8, game_state.spawn_radius)
        sx = game_state.car_world_x + sdist * math.cos(sangle)
        sy = game_state.car_world_y + sdist * math.sin(sangle)
        
        if world.get_terrain_at(sx, sy).get("passable", True):
            new_obstacle = obstacle_class(sx, sy)
            game_state.active_obstacles.append(new_obstacle)
            return
