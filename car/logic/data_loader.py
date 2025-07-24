import importlib.util
import sys

# The default path to the faction data
DEFAULT_FACTIONS_PATH = "car/data/factions.py"
# The path to the temporary, session-specific faction data
TEMP_FACTIONS_PATH = "temp/factions.py"

def load_faction_data():
    """
    Dynamically loads the FACTION_DATA dictionary.

    It first checks if a session-specific 'factions.py' exists in the 'temp/'
    directory. If it does, it loads the FACTION_DATA from there. If not, it
    falls back to loading the default data from 'car/data/factions.py'.

    This allows each new game to have its own unique, LLM-generated set of
    factions while maintaining a stable default for the main menu and other
    pre-game states.
    """
    path_to_load = None
    
    try:
        # Check if the temp file exists and is not empty
        with open(TEMP_FACTIONS_PATH, 'r') as f:
            if f.read().strip():
                path_to_load = TEMP_FACTIONS_PATH
    except (FileNotFoundError, IOError):
        # If the temp file doesn't exist or can't be read, use the default
        pass

    if not path_to_load:
        path_to_load = DEFAULT_FACTIONS_PATH

    # Dynamically import the module from the determined path
    spec = importlib.util.spec_from_file_location("factions_data", path_to_load)
    factions_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(factions_module)
    
    return factions_module.FACTION_DATA

# Load the data once on startup
FACTION_DATA = load_faction_data()
