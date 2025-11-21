import importlib.util
import sys
import json
import os

# --- Constants for File Paths ---
DEFAULT_FACTIONS_PATH = "car/data/factions.py"
TEMP_FACTIONS_PATH = "temp/factions.py"
TEMP_WORLD_DETAILS_PATH = "temp/world_details.json"
TEMP_TRIGGERS_PATH = "temp/triggers.json"


def load_faction_data():
    """
    Dynamically loads the FACTION_DATA dictionary.
    Checks for a session-specific 'factions.py' in 'temp/' and falls back
    to the default if not found.
    """
    path_to_load = DEFAULT_FACTIONS_PATH
    if os.path.exists(TEMP_FACTIONS_PATH):
        # Check if the file is not empty
        if os.path.getsize(TEMP_FACTIONS_PATH) > 0:
            path_to_load = TEMP_FACTIONS_PATH

    spec = importlib.util.spec_from_file_location("factions_data", path_to_load)
    factions_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(factions_module)
    
    return factions_module.FACTION_DATA

def load_world_details_data():
    """
    Loads the world_details.json from the temp/ directory if it exists.
    Returns an empty dictionary if the file is not found.
    """
    if os.path.exists(TEMP_WORLD_DETAILS_PATH):
        try:
            with open(TEMP_WORLD_DETAILS_PATH, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # If the file is corrupted or can't be read, return empty
            return {}
    return {}

def load_triggers_data():
    """
    Loads the triggers.json from the temp/ directory if it exists.
    Returns an empty list if the file is not found.
    """
    if os.path.exists(TEMP_TRIGGERS_PATH):
        try:
            with open(TEMP_TRIGGERS_PATH, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


# Load the data once on startup
FACTION_DATA = load_faction_data()
WORLD_DETAILS_DATA = load_world_details_data()
TRIGGERS_DATA = load_triggers_data()
