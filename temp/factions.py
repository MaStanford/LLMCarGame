FACTION_DATA = {
    "the_vultures": {
        "name": "The Vultures",
        "hub_city_coordinates": [
            -30,
            30
        ],
        "control": 50,
        "relationships": {
            "desert_rats": "Hostile",
            "corporate_guard": "Hostile",
            "the_convoy": "Neutral",
            "the_junction": "Neutral"
        },
        "units": [
            "rust_bucket",
            "raider_buggy",
            "technical"
        ],
        "faction_boss": {
            "name": "Scrap King Klaw",
            "vehicle": "war_rig",
            "hp_multiplier": 5.0,
            "damage_multiplier": 2.5
        }
    },
    "desert_rats": {
        "name": "Desert Rats",
        "hub_city_coordinates": [
            40,
            -20
        ],
        "control": 50,
        "relationships": {
            "the_vultures": "Hostile",
            "corporate_guard": "Hostile",
            "the_convoy": "Allied",
            "the_junction": "Neutral"
        },
        "units": [
            "motorcycle",
            "hotrod",
            "muscle_car"
        ],
        "faction_boss": {
            "name": "Road Captain Fury",
            "vehicle": "sports_car",
            "hp_multiplier": 3.0,
            "damage_multiplier": 3.5
        }
    },
    "corporate_guard": {
        "name": "Corporate Guard",
        "hub_city_coordinates": [
            25,
            50
        ],
        "control": 50,
        "relationships": {
            "the_vultures": "Hostile",
            "desert_rats": "Hostile",
            "the_convoy": "Hostile",
            "the_junction": "Neutral"
        },
        "units": [
            "sedan",
            "armored_truck",
            "peacekeeper"
        ],
        "faction_boss": {
            "name": "Commander Valerius",
            "vehicle": "hatchback",
            "hp_multiplier": 4.0,
            "damage_multiplier": 3.0
        }
    },
    "the_convoy": {
        "name": "The Convoy",
        "hub_city_coordinates": [
            -40,
            -35
        ],
        "control": 50,
        "relationships": {
            "the_vultures": "Neutral",
            "desert_rats": "Allied",
            "corporate_guard": "Hostile",
            "the_junction": "Neutral"
        },
        "units": [
            "truck",
            "van",
            "panel_wagon"
        ],
        "faction_boss": {
            "name": "The Quartermaster",
            "vehicle": "truck",
            "hp_multiplier": 6.0,
            "damage_multiplier": 2.0
        }
    },
    "the_junction": {
        "name": "The Junction",
        "hub_city_coordinates": [
            0,
            0
        ],
        "control": 100,
        "relationships": {
            "the_vultures": "Neutral",
            "desert_rats": "Neutral",
            "corporate_guard": "Neutral",
            "the_convoy": "Neutral"
        },
        "units": [
            "rusty_sedan",
            "guard_truck"
        ],
        "faction_boss": null
    }
}