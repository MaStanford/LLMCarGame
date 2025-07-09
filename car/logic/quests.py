class Objective:
    def __init__(self):
        self.completed = False

    def update(self, game_state):
        pass

class KillBossObjective(Objective):
    def __init__(self, boss_name):
        super().__init__()
        self.boss_name = boss_name

    def update(self, game_state):
        if self.boss_name not in game_state["active_bosses"]:
            self.completed = True

class KillCountObjective(Objective):
    def __init__(self, target_count):
        super().__init__()
        self.target_count = target_count
        self.kill_count = 0

    def update(self, game_state):
        # This will be updated by an external event in game.py
        if self.kill_count >= self.target_count:
            self.completed = True

class SurvivalObjective(Objective):
    def __init__(self, duration, mini_boss_name):
        super().__init__()
        self.duration = duration
        self.timer = duration
        self.mini_boss_name = mini_boss_name
        self.mini_boss_spawned = False

    def update(self, game_state):
        if self.timer > 0:
            self.timer -= 1
        elif not self.mini_boss_spawned:
            # Logic to spawn mini-boss will be in game.py
            self.mini_boss_spawned = True
        
        if self.mini_boss_spawned and self.mini_boss_name not in game_state["active_enemies"]:
            self.completed = True

class Quest:
    def __init__(self, name, description, objectives, rewards):
        self.name = name
        self.description = description
        self.objectives = objectives
        self.rewards = rewards
        self.completed = False

    def update(self, game_state):
        all_completed = True
        for objective in self.objectives:
            objective.update(game_state)
            if not objective.completed:
                all_completed = False
        self.completed = all_completed

# --- Quest Definitions ---
QUESTS = {
    "kill_rick": {
        "name": "Bounty: 'Road Rash' Rick",
        "description": "A notorious bandit named 'Road Rash' Rick has been terrorizing the area. Hunt him down and destroy his vehicle.",
        "objectives": [
            (KillBossObjective, ["boss_rick"]),
        ],
        "rewards": {
            "xp": 1000,
            "cash": 500,
        },
        "boss": {
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
    },
    "clear_the_road": {
        "name": "Clear the Road",
        "description": "Bandits have been blocking a key trade route. Clear out 10 of them to make it safe again.",
        "objectives": [
            (KillCountObjective, [10]),
        ],
        "rewards": {
            "xp": 500,
            "cash": 250,
        }
    },
    "survive_the_onslaught": {
        "name": "Survive the Onslaught",
        "description": "A rival gang is trying to take over your turf. Survive their initial assault and then take out their leader.",
        "objectives": [
            (SurvivalObjective, [3000, "mini_boss_brute"]), # 50ms * 3000 = 150 seconds
        ],
        "rewards": {
            "xp": 1500,
            "cash": 750,
        }
    }
}
