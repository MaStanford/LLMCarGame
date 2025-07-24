# --- Faction Definitions ---

FACTION_DATA = {
    "crimson_cartel": {
        "name": "Crimson Cartel",
        "hub_city_coordinates": (35, 35), # Moved to a remote location
        "control": 50,
        "relationships": {
            "blue_syndicate": "Hostile",
            "salvage_core": "Hostile",
            "rust_prophets": "Hostile",
            "dustwind_caravans": "Hostile",
            "the_junction": "Neutral"
        },
        "units": ["bandit", "marauder", "raider_buggy"],
        "faction_boss": {
            "name": "Mad Murdock",
            "vehicle": "war_rig",
            "hp_multiplier": 6.0,
            "damage_multiplier": 3.0
        }
    },
    "blue_syndicate": {
        "name": "Blue Syndicate",
        "hub_city_coordinates": (10, 10),
        "control": 50,
        "relationships": {
            "crimson_cartel": "Hostile",
            "salvage_core": "Neutral",
            "rust_prophets": "Hostile",
            "dustwind_caravans": "Allied",
            "the_junction": "Neutral"
        },
        "units": ["rusty_sedan", "hatchback", "guard_truck"],
        "faction_boss": {
            "name": "The Chairman",
            "vehicle": "armored_truck",
            "hp_multiplier": 4.0,
            "damage_multiplier": 2.5
        }
    },
    "salvage_core": {
        "name": "The Salvage Core",
        "hub_city_coordinates": (-15, 20),
        "control": 50,
        "relationships": {
            "crimson_cartel": "Hostile",
            "blue_syndicate": "Neutral",
            "rust_prophets": "Hostile",
            "dustwind_caravans": "Neutral",
            "the_junction": "Neutral"
        },
        "units": ["technical", "scav_hauler", "engineer", "miner"],
        "faction_boss": {
            "name": "Vulcan",
            "vehicle": "miner",
            "hp_multiplier": 5.0,
            "damage_multiplier": 2.0
        }
    },
    "rust_prophets": {
        "name": "The Rust Prophets",
        "hub_city_coordinates": (30, -15),
        "control": 50,
        "relationships": {
            "crimson_cartel": "Hostile",
            "blue_syndicate": "Hostile",
            "salvage_core": "Hostile",
            "dustwind_caravans": "Hostile",
            "the_junction": "Hostile" # Hostile to all forms of organized society
        },
        "units": ["rustbucket", "zealot", "war_pulpit"],
        "faction_boss": {
            "name": "The Patriarch",
            "vehicle": "hotrod",
            "hp_multiplier": 3.0,
            "damage_multiplier": 3.5
        }
    },
    "dustwind_caravans": {
        "name": "Dustwind Caravans",
        "hub_city_coordinates": (5, -25),
        "control": 50,
        "relationships": {
            "crimson_cartel": "Hostile",
            "blue_syndicate": "Allied",
            "salvage_core": "Neutral",
            "rust_prophets": "Hostile",
            "the_junction": "Neutral"
        },
        "units": ["outrider", "armored_transport", "war_rig"],
        "faction_boss": {
            "name": "The Road Captain",
            "vehicle": "truck",
            "hp_multiplier": 4.5,
            "damage_multiplier": 2.2
        }
    },
    "the_junction": {
        "name": "The Junction",
        "hub_city_coordinates": (0, 0), # New neutral hub at the center
        "control": 100, # Always stable
        "relationships": {
            "crimson_cartel": "Neutral",
            "blue_syndicate": "Neutral",
            "salvage_core": "Neutral",
            "rust_prophets": "Hostile",
            "dustwind_caravans": "Neutral"
        },
        "units": ["peacekeeper", "patrol_buggy"],
        "faction_boss": None # Neutral faction has no boss
    }
}