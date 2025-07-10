import os
import importlib

ENTITY_BASE_PATH = "car.entities"
VEHICLE_PATH = "vehicles"
CHARACTER_PATH = "characters"
OBSTACLE_PATH = "obstacles"

PLAYER_CARS = []
ENEMY_VEHICLES = []
ENEMY_CHARACTERS = []
FAUNA = []
OBSTACLES = []

def _populate_entities():
    """
    Dynamically discovers and loads all entities from the file system,
    populating the lists of player cars, enemies, and fauna.
    """
    # Player Cars
    player_car_names = [
        "sports_car", "sedan", "van", "truck", "panel_wagon", 
        "hotrod", "motorcycle", "hatchback"
    ]
    for name in player_car_names:
        _load_entity(VEHICLE_PATH, name, PLAYER_CARS)

    # Enemy Vehicles
    enemy_vehicle_names = ["rusty_sedan", "muscle_car", "armored_truck"]
    for name in enemy_vehicle_names:
        _load_entity(VEHICLE_PATH, name, ENEMY_VEHICLES)

    # Enemy Characters
    enemy_character_names = ["bandit", "marauder"]
    for name in enemy_character_names:
        _load_entity(CHARACTER_PATH, name, ENEMY_CHARACTERS)

    # Fauna
    fauna_names = ["dog", "cat", "cow"]
    for name in fauna_names:
        _load_entity(CHARACTER_PATH, name, FAUNA)

    # Obstacles
    obstacle_names = ["rock", "oil_barrel"]
    for name in obstacle_names:
        _load_entity(OBSTACLE_PATH, name, OBSTACLES)

def _load_entity(entity_type_path, name, entity_list):
    """Helper to load an entity class and add it to a list."""
    try:
        module_path = f"{ENTITY_BASE_PATH}.{entity_type_path}.{name}"
        module = importlib.import_module(module_path)
        class_name = "".join(word.capitalize() for word in name.split("_"))
        entity_class = getattr(module, class_name)
        entity_list.append(entity_class)
    except (ImportError, AttributeError) as e:
        # This should not happen if the file structure is correct
        print(f"Warning: Could not load entity '{name}': {e}")

# Initial population of the entity lists
_populate_entities()
