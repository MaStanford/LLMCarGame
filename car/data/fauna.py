FAUNA_DATA = [
    {
        "name": "Quest Giver",
        "art": [
            " O ",
            "/|\\",
            "/ \\"
        ],
        "hp": 100,
        "spawn_rate": 0.1,
        "type": "quest_giver"
    },
    {
        "name": "Deer",
        "art": [
            " /\\ ",
            "(oo)",
            " vv "
        ],
        "hp": 25,
        "spawn_rate": 0.5,
        "type": "neutral"
    },
    {
        "name": "Bandit",
        "art": [
            " x ",
            "/|\\",
            "/ \\"
        ],
        "hp": 50,
        "spawn_rate": 0.3,
        "type": "hostile"
    }
]

TOTAL_FAUNA_SPAWN_RATE = sum(f["spawn_rate"] for f in FAUNA_DATA)
