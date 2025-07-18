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
    def __init__(self, name, description, objectives, rewards, city_id=None, quest_giver_faction=None, target_faction=None, time_limit=None):
        self.name = name
        self.description = description
        self.objectives = objectives
        self.rewards = rewards
        self.city_id = city_id
        self.quest_giver_faction = quest_giver_faction
        self.target_faction = target_faction
        self.time_limit = time_limit
        self.completed = False
        self.failed = False

    def update(self, game_state):
        if self.time_limit is not None:
            self.time_limit -= 1
            if self.time_limit <= 0:
                self.failed = True
                return

        all_completed = True
        for objective in self.objectives:
            objective.update(game_state)
            if not objective.completed:
                all_completed = False
        self.completed = all_completed

# --- Quest Templates ---
QUEST_TEMPLATES = {
    "raid_convoy": {
        "name": "Raid Convoy: {target_faction_name}",
        "description": "The {quest_giver_faction_name} wants you to disrupt a supply convoy from the {target_faction_name}. Destroy 5 of their transport vehicles.",
        "objectives": [
            (KillCountObjective, [5]),
        ],
        "rewards": {
            "xp": 750,
            "cash": 300,
        },
        "time_limit": 3600 # 2 minutes
    },
    "assassinate_rival": {
        "name": "Assassinate: {target_faction_name} Captain",
        "description": "Take out a high-value target from the {target_faction_name}. They are leading a patrol in this sector.",
        "objectives": [
            (KillBossObjective, ["faction_captain"]),
        ],
        "rewards": {
            "xp": 1200,
            "cash": 600,
        },
        "boss": {
            "name": "{target_faction_name} Captain",
            "car": "muscle_car",
            "hp_multiplier": 2.5,
            "damage_multiplier": 1.8,
            "xp_value": 600,
            "cash_value": 300,
        },
        "time_limit": 4800 # 2.6 minutes
    },
    "defend_outpost": {
        "name": "Defend Outpost from {target_faction_name}",
        "description": "An outpost is under attack from the {target_faction_name}. Hold them off until reinforcements arrive.",
        "objectives": [
            (SurvivalObjective, [3000, "rival_lieutenant"]), # 150 seconds
        ],
        "rewards": {
            "xp": 1000,
            "cash": 500,
        }
    }
}
