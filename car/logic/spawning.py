import random
import math
from .entity_loader import ENEMY_VEHICLES, ENEMY_CHARACTERS, FAUNA, OBSTACLES
from ..data.game_constants import CITY_SPACING, CITY_SIZE
from ..data.factions import FACTION_DATA
from ..world.generation import get_city_faction

def _get_distance_to_nearest_city_center(x, y):
    """Calculates the distance to the nearest city center."""
    grid_x = round(x / CITY_SPACING)
    grid_y = round(y / CITY_SPACING)
    city_center_x = grid_x * CITY_SPACING
    city_center_y = grid_y * CITY_SPACING
    return math.sqrt((x - city_center_x)**2 + (y - city_center_y)**2)

def spawn_enemy(game_state, world):
    """Spawns a new enemy based on proximity to city, faction alignment, and difficulty."""
    max_enemies = game_state.difficulty_mods.get("max_enemies", 5)
    if len(game_state.active_enemies) >= max_enemies:
        return

    # Determine current faction territory and player's reputation
    current_faction_id = get_city_faction(game_state.car_world_x, game_state.car_world_y)
    player_rep = game_state.faction_reputation.get(current_faction_id, 0)

    # Determine spawn rate based on location and reputation
    dist_to_city = _get_distance_to_nearest_city_center(game_state.car_world_x, game_state.car_world_y)
    
    base_spawn_chance = min(1.0, (dist_to_city - CITY_SIZE) / (CITY_SPACING / 2))
    
    if dist_to_city < CITY_SIZE: # Inside a city
        if player_rep >= 50: # Friendly Hub City
            spawn_chance = 0.0
        elif player_rep <= -50: # Hostile Hub City
            spawn_chance = base_spawn_chance * 2.0
        else: # Neutral or allied town
            spawn_chance = base_spawn_chance * 0.25
    else: # Wilderness
        spawn_chance = base_spawn_chance

    if random.random() > spawn_chance:
        return

    # Determine which faction's units to spawn
    faction_units = FACTION_DATA[current_faction_id]["units"]
    enemy_name = random.choice(faction_units)
    
    # Find the corresponding enemy class
    enemy_class = next((e for e in ENEMY_VEHICLES + ENEMY_CHARACTERS if e.__name__.lower() == enemy_name.lower()), None)

    if not enemy_class:
        return # Should not happen if data is correct

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
