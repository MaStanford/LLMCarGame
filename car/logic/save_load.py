import os
import shutil
import json
from ..game_state import GameState

SAVES_DIR = "saves"
TEMP_DIR = "temp"
GAME_STATE_FILE = "save_game.json"
FACTIONS_FILE = "factions.py"
QUEST_LOG_FILE = "quest_log.json"

def get_save_slots():
    """Returns a list of available save slot names."""
    if not os.path.exists(SAVES_DIR):
        return []
    return sorted([d for d in os.listdir(SAVES_DIR) if os.path.isdir(os.path.join(SAVES_DIR, d))])

def save_game(game_state, save_name):
    """
    Saves the current game session to a named save slot.
    
    This involves creating a new directory for the save slot and copying all
    dynamically generated session files from the 'temp/' directory into it.
    """
    if not save_name:
        return # Can't save without a name

    save_slot_dir = os.path.join(SAVES_DIR, save_name)
    
    # Create the save slot directory, overwriting if it exists
    if os.path.exists(save_slot_dir):
        shutil.rmtree(save_slot_dir)
    os.makedirs(save_slot_dir)

    # --- 1. Save the core GameState object ---
    # We need a custom serializer for the GameState
    game_state_dict = game_state.to_dict()
    with open(os.path.join(save_slot_dir, GAME_STATE_FILE), "w") as f:
        json.dump(game_state_dict, f, indent=4)

    # --- 2. Copy dynamic world files from temp to the save slot ---
    for filename in [FACTIONS_FILE, QUEST_LOG_FILE]:
        temp_path = os.path.join(TEMP_DIR, filename)
        if os.path.exists(temp_path):
            shutil.copy(temp_path, save_slot_dir)

def load_game(save_name):
    """
    Loads a game session from a named save slot.

    This involves clearing the 'temp/' directory and copying all files
    from the save slot into it, ensuring the session runs on the correct
    world data.
    """
    save_slot_dir = os.path.join(SAVES_DIR, save_name)
    if not os.path.exists(save_slot_dir):
        return None # Save not found

    # --- 1. Clear the temp directory ---
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)

    # --- 2. Copy all files from the save slot to temp ---
    for item in os.listdir(save_slot_dir):
        s = os.path.join(save_slot_dir, item)
        d = os.path.join(TEMP_DIR, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks=True)
        else:
            shutil.copy2(s, d)
            
    # --- 3. Load the dynamic faction data ---
    # This is a bit tricky since it's a .py file, not JSON
    # We can use importlib to load it dynamically
    import importlib.util
    import sys
    
    factions_data = {}
    factions_path = os.path.join(TEMP_DIR, FACTIONS_FILE)
    if os.path.exists(factions_path):
        spec = importlib.util.spec_from_file_location("temp_factions", factions_path)
        temp_factions_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(temp_factions_module)
        factions_data = temp_factions_module.FACTION_DATA
        # Clean up from sys.modules to allow for future loads
        del sys.modules["temp_factions"]


    # --- 4. Load the GameState object ---
    game_state_path = os.path.join(TEMP_DIR, GAME_STATE_FILE)
    with open(game_state_path, "r") as f:
        game_state_dict = json.load(f)
    
    # Pass the loaded faction data to the constructor
    return GameState.from_dict(game_state_dict, factions_data)