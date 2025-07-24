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
        # A boss is just a powerful enemy, so we check the active_enemies list
        if not any(enemy.name == self.boss_name for enemy in game_state.active_enemies):
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
    def __init__(self, name, description, objectives, rewards, city_id=None, quest_giver_faction=None, target_faction=None, time_limit=None, next_quest_id=None, requires_turn_in=True, dialog=None, is_conquest_quest=False):
        self.name = name
        self.description = description
        self.objectives = objectives
        self.rewards = rewards
        self.city_id = city_id
        self.quest_giver_faction = quest_giver_faction
        self.target_faction = target_faction
        self.time_limit = time_limit
        self.next_quest_id = next_quest_id
        self.requires_turn_in = requires_turn_in
        self.dialog = dialog if dialog else "An old friend has a new job for you."
        self.is_conquest_quest = is_conquest_quest
        self.completed = False
        self.failed = False
        self.ready_to_turn_in = False

    def to_dict(self):
        """Serializes the quest to a dictionary for logging."""
        return {
            "name": self.name,
            "description": self.description,
            "quest_giver_faction": self.quest_giver_faction,
            "target_faction": self.target_faction,
        }

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
        "offer_dialog": "Their supply lines are stretched thin. A surgical strike now could cripple their operations in this sector. Can you handle it?",
        "detail_dialog": "We've received intel about a lightly-guarded supply convoy moving through this area. Your mission is to intercept and destroy five of their transport vehicles. Expect resistance, but we have faith in your abilities.",
        "completion_dialog": "Excellent work. Their supply chain is in chaos. This will give us the opening we need. Here is your payment.",
        "objectives": [
            (KillCountObjective, [5]),
        ],
        "rewards": {
            "xp": 750,
            "cash": 300,
        },
        "time_limit": 3600, # 2 minutes
        "next_quest_id": "assassinate_rival"
    },
    "assassinate_rival": {
        "name": "Assassinate: {target_faction_name} Captain",
        "description": "Take out a high-value target from the {target_faction_name}. They are leading a patrol in this sector.",
        "offer_dialog": "A rival captain has been a thorn in our side for too long. We need someone to permanently remove them from the board. Are you up for it?",
        "detail_dialog": "This won't be easy. The target is a seasoned veteran in a modified Muscle Car. They'll be heavily armed and likely have an escort. Find them, eliminate them, and send a message.",
        "completion_dialog": "They won't be bothering us anymore. You've done us a great service. Here's your reward.",
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
        "offer_dialog": "We're in a tight spot! Our outpost is being overrun. We need you to hold the line until our reinforcements can get there. Can you do it?",
        "detail_dialog": "The enemy is throwing everything they have at us. Survive their assault for a few minutes. A lieutenant is leading the final wave; take them out to break their morale and secure the outpost.",
        "completion_dialog": "You saved those people! We were cutting it close, but you bought us the time we needed. We're in your debt.",
        "objectives": [
            (SurvivalObjective, [3000, "rival_lieutenant"]), # 150 seconds
        ],
        "rewards": {
            "xp": 1000,
            "cash": 500,
        }
    }
}
