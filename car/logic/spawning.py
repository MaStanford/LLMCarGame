import random
import math
import logging
from .entity_loader import ENEMY_VEHICLES, ENEMY_CHARACTERS, FAUNA, OBSTACLES
from ..data.game_constants import CITY_SPACING, CITY_SIZE
from ..data.factions import FACTION_DATA
from ..world.generation import get_city_faction

def spawn_initial_entities(game_state, world):
    """Spawns an initial dense field of entities around the player."""
    logging.info("SPAWN: Spawning initial entities.")
    # Spawn a larger number of obstacles and fauna in a wider radius
    for _ in range(30): # More entities for the initial spawn
        spawn_obstacle(game_state, world, is_initial_spawn=True)
        spawn_fauna(game_state, world, is_initial_spawn=True)

def _get_distance_to_nearest_city_center(x, y):
    """Calculates the distance to the nearest city center."""
    grid_x = round(x / CITY_SPACING)
    grid_y = round(y / CITY_SPACING)
    city_center_x = grid_x * CITY_SPACING
    city_center_y = grid_y * CITY_SPACING
    return math.sqrt((x - city_center_x)**2 + (y - city_center_y)**2)

def spawn_enemy(game_state, world):
    """Spawns a new enemy based on proximity to city, faction alignment, and difficulty."""
    logging.info("SPAWN: Attempting to spawn enemy.")
    max_enemies = game_state.difficulty_mods.get("max_enemies", 5)
    if len(game_state.active_enemies) >= max_enemies:
        logging.info(f"SPAWN: Max enemies ({max_enemies}) reached. Aborting.")
        return

    # Determine current faction territory and player's reputation
    current_faction_id = get_city_faction(game_state.car_world_x, game_state.car_world_y)
    player_rep = game_state.faction_reputation.get(current_faction_id, 0)
    logging.info(f"SPAWN: Faction: {current_faction_id}, Player Rep: {player_rep}")

    # Determine spawn rate based on location and reputation
    dist_to_city = _get_distance_to_nearest_city_center(game_state.car_world_x, game_state.car_world_y)
    logging.info(f"SPAWN: Distance to city: {dist_to_city:.2f}")
    
    base_spawn_chance = min(1.0, max(0, dist_to_city - CITY_SIZE) / (CITY_SPACING / 2))
    
    if dist_to_city < CITY_SIZE: # Inside a city
        logging.info("SPAWN: Inside a city.")
        if player_rep >= 50: # Friendly Hub City
            spawn_chance = 0.0
            logging.info("SPAWN: Friendly Hub City, spawn chance 0.")
        elif player_rep <= -50: # Hostile Hub City
            spawn_chance = base_spawn_chance * 2.0
            logging.info(f"SPAWN: Hostile Hub City, spawn chance {spawn_chance:.2f}.")
        else: # Neutral or allied town
            spawn_chance = base_spawn_chance * 0.25
            logging.info(f"SPAWN: Neutral/Allied Town, spawn chance {spawn_chance:.2f}.")
    else: # Wilderness
        spawn_chance = base_spawn_chance
        logging.info(f"SPAWN: In wilderness, spawn chance {spawn_chance:.2f}.")

    if random.random() > spawn_chance:
        logging.info(f"SPAWN: Random roll failed. Aborting.")
        return

    # Decide whether to spawn a vehicle or a character (e.g., 70/30 split)
    if random.random() < 0.7:
        # Spawn a faction-specific vehicle
        faction_units = FACTION_DATA[current_faction_id]["units"]
        possible_vehicles = [unit for unit in faction_units if any(e.__name__.lower() == unit.lower() for e in ENEMY_VEHICLES)]
        if not possible_vehicles:
            logging.warning(f"SPAWN: No vehicles defined for faction '{current_faction_id}'.")
            return
        enemy_name = random.choice(possible_vehicles)
        logging.info(f"SPAWN: Selected vehicle: {enemy_name}")
        enemy_class = next((e for e in ENEMY_VEHICLES if e.__name__.lower() == enemy_name.lower()), None)
    else:
        # Spawn a random character (neutral)
        enemy_class = random.choice(ENEMY_CHARACTERS)
        enemy_name = enemy_class.__name__
        logging.info(f"SPAWN: Selected character: {enemy_name}")

    if not enemy_class:
        logging.error(f"SPAWN: Could not find enemy class for '{enemy_name}'.")
        return

    # Find a valid spawn location
    for i in range(10):
        sangle = random.uniform(0, 2 * math.pi)
        sdist = random.uniform(game_state.spawn_radius * 0.8, game_state.spawn_radius)
        sx = game_state.car_world_x + sdist * math.cos(sangle)
        sy = game_state.car_world_y + sdist * math.sin(sangle)
        
        if world.get_terrain_at(sx, sy).get("passable", True):
            logging.info(f"SPAWN: Spawning {enemy_name} at ({sx:.2f}, {sy:.2f}).")
            new_enemy = enemy_class(sx, sy)
            game_state.active_enemies.append(new_enemy)
            return
    logging.warning("SPAWN: Could not find a valid spawn location after 10 attempts.")

def spawn_fauna(game_state, world, is_initial_spawn=False):
    """Spawns a new fauna."""
    fauna_class = random.choice(FAUNA)
    
    # Determine spawn radius
    if is_initial_spawn:
        min_dist = 10 # Spawn closer for the initial batch
        max_dist = game_state.spawn_radius * 1.2
    else:
        min_dist = game_state.spawn_radius # Spawn just off-screen
        max_dist = game_state.despawn_radius * 0.9 # But not so far they despawn
    
    # Find a valid spawn location
    for _ in range(10):
        sangle = random.uniform(0, 2 * math.pi)
        sdist = random.uniform(min_dist, max_dist)
        sx = game_state.car_world_x + sdist * math.cos(sangle)
        sy = game_state.car_world_y + sdist * math.sin(sangle)
        
        if world.get_terrain_at(sx, sy).get("passable", True):
            new_fauna = fauna_class(sx, sy)
            game_state.active_fauna.append(new_fauna)
            return

def spawn_obstacle(game_state, world, is_initial_spawn=False):
    """Spawns a new obstacle."""
    obstacle_class = random.choice(OBSTACLES)
    
    # Determine spawn radius
    if is_initial_spawn:
        min_dist = 10 # Spawn closer for the initial batch
        max_dist = game_state.spawn_radius * 1.2
    else:
        min_dist = game_state.spawn_radius # Spawn just off-screen
        max_dist = game_state.despawn_radius * 0.9 # But not so far they despawn

    # Find a valid spawn location
    for _ in range(10):
        sangle = random.uniform(0, 2 * math.pi)
        sdist = random.uniform(min_dist, max_dist)
        sx = game_state.car_world_x + sdist * math.cos(sangle)
        sy = game_state.car_world_y + sdist * math.sin(sangle)
        
        if world.get_terrain_at(sx, sy).get("passable", True):
            new_obstacle = obstacle_class(sx, sy)
            game_state.active_obstacles.append(new_obstacle)
            return

