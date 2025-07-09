class Quest:
    def __init__(self, name, description, objectives, rewards):
        self.name = name
        self.description = description
        self.objectives = objectives
        self.rewards = rewards
        self.completed = False

    def is_completed(self, game_state):
        for objective in self.objectives:
            if not objective.is_completed(game_state):
                return False
        return True

class KillBossObjective:
    def __init__(self, boss_name):
        self.boss_name = boss_name

    def is_completed(self, game_state):
        return self.boss_name not in game_state["active_bosses"]

# --- Quest Definitions ---
QUESTS = {
    "kill_boss": {
        "name": "Bounty: 'Road Rash' Rick",
        "description": "A notorious bandit named 'Road Rash' Rick has been terrorizing the area. Hunt him down and destroy his vehicle.",
        "objectives": [
            {"type": "kill", "target": "boss_rick"},
        ],
        "rewards": {
            "xp": 1000,
            "cash": 500,
        }
    }
}

# --- Boss Definitions ---
BOSSES = {
    "boss_rick": {
        "name": "'Road Rash' Rick",
        "car": "hotrod", # Uses a car from CARS_DATA
        "hp_multiplier": 2.0,
        "damage_multiplier": 1.5,
        "xp_value": 500,
        "cash_value": 250,
        "art": [
            r"   ______   ",
            r"  / _  _ \  ",
            r" |(o)(o)| ",
            r" |  \/  | ",
            r"  \____/  ",
        ]
    }
}
