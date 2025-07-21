# --- Faction Definitions ---

FACTION_DATA = {
    "crimson_cartel": {
        "name": "Crimson Cartel",
        "hub_city_coordinates": (35, 35), # Moved to a remote location
        "relationships": {
            "blue_syndicate": "Hostile",
            "salvage_core": "Hostile",
            "rust_prophets": "Hostile",
            "dustwind_caravans": "Hostile",
            "the_junction": "Neutral"
        },
        "units": ["bandit", "marauder", "raider_buggy"]
    },
    "blue_syndicate": {
        "name": "Blue Syndicate",
        "hub_city_coordinates": (10, 10),
        "relationships": {
            "crimson_cartel": "Hostile",
            "salvage_core": "Neutral",
            "rust_prophets": "Hostile",
            "dustwind_caravans": "Allied",
            "the_junction": "Neutral"
        },
        "units": ["rusty_sedan", "hatchback", "guard_truck"]
    },
    "salvage_core": {
        "name": "The Salvage Core",
        "hub_city_coordinates": (-15, 20),
        "relationships": {
            "crimson_cartel": "Hostile",
            "blue_syndicate": "Neutral",
            "rust_prophets": "Hostile",
            "dustwind_caravans": "Neutral",
            "the_junction": "Neutral"
        },
        "units": ["technical", "scav_hauler", "engineer", "miner"]
    },
    "rust_prophets": {
        "name": "The Rust Prophets",
        "hub_city_coordinates": (30, -15),
        "relationships": {
            "crimson_cartel": "Hostile",
            "blue_syndicate": "Hostile",
            "salvage_core": "Hostile",
            "dustwind_caravans": "Hostile",
            "the_junction": "Hostile" # Hostile to all forms of organized society
        },
        "units": ["rustbucket", "zealot", "war_pulpit"]
    },
    "dustwind_caravans": {
        "name": "Dustwind Caravans",
        "hub_city_coordinates": (5, -25),
        "relationships": {
            "crimson_cartel": "Hostile",
            "blue_syndicate": "Allied",
            "salvage_core": "Neutral",
            "rust_prophets": "Hostile",
            "the_junction": "Neutral"
        },
        "units": ["outrider", "armored_transport", "war_rig"]
    },
    "the_junction": {
        "name": "The Junction",
        "hub_city_coordinates": (0, 0), # New neutral hub at the center
        "relationships": {
            "crimson_cartel": "Neutral",
            "blue_syndicate": "Neutral",
            "salvage_core": "Neutral",
            "rust_prophets": "Hostile",
            "dustwind_caravans": "Neutral"
        },
        "units": ["peacekeeper", "patrol_buggy"]
    }
}
