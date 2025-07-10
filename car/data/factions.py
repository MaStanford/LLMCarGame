# --- Faction Definitions ---

FACTION_DATA = {
    "crimson_cartel": {
        "name": "Crimson Cartel",
        "hub_city_coordinates": (0, 0),
        "relationships": {
            "blue_syndicate": "Hostile"
        },
        "units": ["bandit", "marauder"]
    },
    "blue_syndicate": {
        "name": "Blue Syndicate",
        "hub_city_coordinates": (10, 10),
        "relationships": {
            "crimson_cartel": "Hostile"
        },
        "units": ["rusty_sedan", "hatchback"]
    }
}
