import json
import os
import logging

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "generation_mode": "local"  # "local" or "gemini_cli"
}

def save_settings(settings: dict):
    """Saves the settings dictionary to the JSON file."""
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
    except IOError as e:
        logging.error(f"Error saving settings to {SETTINGS_FILE}: {e}")

def load_settings() -> dict:
    """Loads the settings dictionary from the JSON file."""
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
            # Ensure all default keys are present
            for key, value in DEFAULT_SETTINGS.items():
                settings.setdefault(key, value)
            return settings
    except (IOError, json.JSONDecodeError) as e:
        logging.error(f"Error loading settings from {SETTINGS_FILE}: {e}. Using default settings.")
        return DEFAULT_SETTINGS
