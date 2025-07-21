import random
from ..vehicle import Vehicle
from ...logic.ai_behaviors import _execute_chase_behavior, _execute_deploy_mine_behavior, _execute_patrol_behavior

class Miner(Vehicle):
    def __init__(self, x, y):
        art = {
            "N": [" 🚚 ", "🚚🚚🚚", " 🚚 "],
            "NE": [" 🚚 ", "🚚🚚🚚", " 🚚 "],
            "E": [" 🚚 ", "🚚🚚🚚", " 🚚 "],
            "SE": [" 🚚 ", "🚚🚚🚚", " 🚚 "],
            "S": [" 🚚 ", "🚚🚚🚚", " 🚚 "],
            "SW": [" 🚚 ", "🚚🚚🚚", " 🚚 "],
            "W": [" 🚚 ", "🚚🚚🚚", " 🚚 "],
            "NW": [" 🚚 ", "🚚🚚🚚", " 🚚 "],
        }
        super().__init__(x, y, art, durability=60, speed=0.3, acceleration=0.02, handling=0.1)
        self.xp_value = 30
        self.cash_value = 40
        self.phases = [
            {"name": "Chase", "duration": (3, 5), "behavior": "CHASE", "next_phases": {"Deploy": 1.0}},
            {"name": "Deploy", "duration": (2, 3), "behavior": "DEPLOY_MINE", "next_phases": {"Patrol": 1.0}},
            {"name": "Patrol", "duration": (4, 6), "behavior": "PATROL", "next_phases": {"Chase": 1.0}}
        ]
        self._initialize_ai()

    def _initialize_ai(self):
        self.current_phase = self.phases[0]
        self.phase_timer = random.uniform(self.current_phase["duration"][0], self.current_phase["duration"][1])

    def update(self, game_state, world):
        self.phase_timer -= 1 / 30.0 # Assuming 30 FPS

        if self.phase_timer <= 0:
            next_phase_options = list(self.current_phase["next_phases"].keys())
            next_phase_weights = list(self.current_phase["next_phases"].values())
            new_phase_name = random.choices(next_phase_options, weights=next_phase_weights, k=1)[0]
            self.current_phase = next((p for p in self.phases if p["name"] == new_phase_name), self.phases[0])
            self.phase_timer = random.uniform(self.current_phase["duration"][0], self.current_phase["duration"][1])

        behavior = self.current_phase["behavior"]
        if behavior == "CHASE":
            _execute_chase_behavior(self, game_state, self)
        elif behavior == "DEPLOY_MINE":
            _execute_deploy_mine_behavior(self, game_state, self)
        elif behavior == "PATROL":
            _execute_patrol_behavior(self, game_state, self)
            
        # Update position
        self.x += self.vx
        self.y += self.vy
