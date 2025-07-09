FAUNA_DATA = [
    {
        "name": "Deer",
        "art": [
            "  __  ",
            " (oo) ",
            " /--\\ ",
            "|    |",
            "|    |",
            " `ww' ",
        ],
        "type": "neutral", "hp": 20, "damage": 0, "speed": 1, "spawn_rate": 0.5,
        "min_dist": 50, "max_dist": 100, "xp_value": 1
    },
    {
        "name": "Dog",
        "art": [
            "  / \\__ ",
            " (    @\\___",
            " /         O",
            "/   (_____/",
            "/_____/   U",
        ],
        "type": "hostile", "hp": 15, "damage": 5, "speed": 1.5, "spawn_rate": 0.3,
        "min_dist": 40, "max_dist": 90, "xp_value": 5
    },
    {
        "name": "Quest Giver",
        "art": [
            "  O  ",
            " /|\\ ",
            " / \\ ",
        ],
        "type": "quest_giver", "hp": 100, "damage": 0, "speed": 0, "spawn_rate": 0.2,
        "min_dist": 20, "max_dist": 70, "xp_value": 0
    }
]

TOTAL_FAUNA_SPAWN_RATE = sum(f["spawn_rate"] for f in FAUNA_DATA)
