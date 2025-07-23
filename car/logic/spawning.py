import random
import math
from .entity_loader import ENEMY_VEHICLES, ENEMY_CHARACTERS, FAUNA, OBSTACLES
from ..data.game_constants import CITY_SPACING, CITY_SIZE, SAFE_ZONE_RADIUS, DESPAWN_RADIUS
from ..data.factions import FACTION_DATA
from ..world.generation import get_city_faction

def _get_distance_to_nearest_city_center(x, y):
    """Calculates the distance to the nearest city center."""
    grid_x = round(x / CITY_SPACING)
    grid_y = round(y / CITY_SPACING)
    city_center_x = grid_x * CITY_SPACING
    city_center_y = grid_y * CITY_SPACING
    return math.sqrt((x - city_center_x)**2 + (y - city_center_y)**2)

def spawn_initial_entities(game_state, world):
    """Spawns an initial dense field of entities around the player."""
    # Spawn a larger number of obstacles and fauna in a wider radius
    for _ in range(100): # More entities for the initial spawn
        spawn_obstacle(game_state, world, is_initial_spawn=True)
        spawn_fauna(game_state, world, is_initial_spawn=True)

def _get_spawn_coordinates(game_state):
    """
    Finds a random (x, y) coordinate that is outside the safe zone
    but inside the despawn radius, ensuring a sparse distribution.
    """
    for _ in range(30): # 30 attempts to find a valid spot
        # Pick a random point in a square around the player
        dx = random.uniform(-DESPAWN_RADIUS, DESPAWN_RADIUS)
        dy = random.uniform(-DESPAWN_RADIUS, DESPAWN_RADIUS)
        
        # Check if the point is outside the safe zone
        if dx**2 + dy**2 > SAFE_ZONE_RADIUS**2:
            return game_state.car_world_x + dx, game_state.car_world_y + dy
            
    return None, None # Failed to find a spot

def spawn_enemy(game_state, world):
    """Spawns a new enemy."""
    max_enemies = game_state.difficulty_mods.get("max_enemies", 5)
    if len(game_state.active_enemies) >= max_enemies:
        return

    # Determine current faction territory and player's reputation
    current_faction_id = get_city_faction(game_state.car_world_x, game_state.car_world_y)
    player_rep = game_state.faction_reputation.get(current_faction_id, 0)

    # Determine spawn rate based on location and reputation
    dist_to_city = _get_distance_to_nearest_city_center(game_state.car_world_x, game_state.car_world_y)
    
    base_spawn_chance = min(1.0, max(0, dist_to_city - CITY_SIZE) / (CITY_SPACING / 2))
    
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

    # Decide whether to spawn a vehicle or a character (e.g., 70/30 split)
    if random.random() < 0.7:
        # Spawn a faction-specific vehicle
        faction_units = FACTION_DATA[current_faction_id]["units"]
        possible_vehicles = [unit for unit in faction_units if any(e.__name__.lower() == unit.lower() for e in ENEMY_VEHICLES)]
        if not possible_vehicles:
            return
        enemy_name = random.choice(possible_vehicles)
        enemy_class = next((e for e in ENEMY_VEHICLES if e.__name__.lower() == enemy_name.lower()), None)
    else:
        # Spawn a random character (neutral)
        enemy_class = random.choice(ENEMY_CHARACTERS)
        enemy_name = enemy_class.__name__

    if not enemy_class:
        return

    sx, sy = _get_spawn_coordinates(game_state)
    if sx is None: return # Could not find a valid spawn point

    if world.get_terrain_at(sx, sy).get("passable", True):
        new_enemy = enemy_class(sx, sy)
        new_enemy.patrol_target_x = sx + random.uniform(-100, 100)
        new_enemy.patrol_target_y = sy + random.uniform(-100, 100)
        game_state.active_enemies.append(new_enemy)

def spawn_fauna(game_state, world, is_initial_spawn=False):
    """Spawns a new fauna."""
    fauna_class = random.choice(FAUNA)
    sx, sy = _get_spawn_coordinates(game_state)
    if sx is None: return

    if world.get_terrain_at(sx, sy).get("passable", True):
        new_fauna = fauna_class(sx, sy)
        game_state.active_fauna.append(new_fauna)

def spawn_obstacle(game_state, world, is_initial_spawn=False):
    """Spawns a new obstacle."""
    obstacle_class = random.choice(OBSTACLES)
    sx, sy = _get_spawn_coordinates(game_state)
    if sx is None: return

    if world.get_terrain_at(sx, sy).get("passable", True):
        new_obstacle = obstacle_class(sx, sy)
        game_state.active_obstacles.append(new_obstacle)
