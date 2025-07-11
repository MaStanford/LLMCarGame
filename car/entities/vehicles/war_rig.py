import random
from ..vehicle import Vehicle
from ...logic.ai_behaviors import _execute_chase_behavior, _execute_evade_behavior, _execute_deploy_mine_behavior

class WarRig(Vehicle):
    """
    The formidable command vehicle of the Dustwind Caravans.
    It's slow but heavily armored, lays mines, and can defend itself.
    """
    def __init__(self, x, y):
        art = [
            "   ▄▄▄▄▄▄▄▄▄▄▄   ",
            " ◢█████████████◣ ",
            "█████████████████",
            "(●)═(●)═════(●)═(●)"
        ]
        super().__init__(x, y, art, durability=500, speed=0.3, acceleration=0.1, handling=0.1)
        self.phases = [
            {"name": "Advance", "duration": (8, 10), "behavior": "CHASE", "next_phases": {"DeployMines": 0.7, "Evade": 0.3}},
            {"name": "DeployMines", "duration": (2, 3), "behavior": "DEPLOY_MINE", "next_phases": {"Advance": 1.0}},
            {"name": "Evade", "duration": (4, 5), "behavior": "EVADE", "next_phases": {"Advance": 1.0}}
        ]
        self._initialize_ai()

    def _initialize_ai(self):
        self.current_phase = self.phases[0]
        self.phase_timer = random.uniform(*self.current_phase["duration"])

    def update(self, game_state, world):
        self.phase_timer -= 1 / 30.0

        if self.phase_timer <= 0:
            next_phase_options = list(self.current_phase["next_phases"].keys())
            next_phase_weights = list(self.current_phase["next_phases"].values())
            new_phase_name = random.choices(next_phase_options, weights=next_phase_weights, k=1)[0]
            self.current_phase = next((p for p in self.phases if p["name"] == new_phase_name), self.phases[0])
            self.phase_timer = random.uniform(*self.current_phase["duration"])

        behavior = self.current_phase["behavior"]
        if behavior == "CHASE":
            _execute_chase_behavior(self, game_state, self)
        elif behavior == "EVADE":
            _execute_evade_behavior(self, game_state, self)
        elif behavior == "DEPLOY_MINE":
            _execute_deploy_mine_behavior(self, game_state, self)
        
        self.x += self.vx
        self.y += self.vy

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY_DUSTWIND", 0), transparent_bg=True)
