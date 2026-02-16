import random
from ..vehicle import Vehicle
from ...logic.ai_behaviors import execute_behavior

from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

class Miner(Vehicle):
    """
    A heavy, armored vehicle that lays mines.
    """
    def __init__(self, x, y):
        art = [
            " /MM\\ ",
            "|MMMM|",
            " \\MM/ "
        ]
        super().__init__(x, y, art, durability=150, speed=2.85 * GLOBAL_SPEED_MULTIPLIER, acceleration=0.3, handling=0.05)
        self.name = "Miner"
        self.collision_damage = 10
        self.shoot_damage = 0
        self.xp_value = 60
        self.cash_value = 80
        self.drop_item = "mine"
        self.drop_rate = 0.4
        self.phases = [
            {"name": "Advance", "duration": (5, 8), "behavior": "CHASE", "next_phases": {"DeployMines": 1.0}},
            {"name": "DeployMines", "duration": (2, 3), "behavior": "DEPLOY_MINE", "next_phases": {"Evade": 0.5, "Advance": 0.5}},
            {"name": "Evade", "duration": (3, 4), "behavior": "EVADE", "next_phases": {"Advance": 1.0}}
        ]
        self._initialize_ai()

    def _initialize_ai(self):
        self.current_phase = self.phases[0]
        self.phase_timer = random.uniform(*self.current_phase["duration"])

    def update(self, game_state, world, dt):
        self.ai_state["elapsed"] = self.ai_state.get("elapsed", 0) + dt

        self.phase_timer -= dt

        if self.phase_timer <= 0:
            next_phase_options = list(self.current_phase["next_phases"].keys())
            next_phase_weights = list(self.current_phase["next_phases"].values())
            new_phase_name = random.choices(next_phase_options, weights=next_phase_weights, k=1)[0]
            self.current_phase = next((p for p in self.phases if p["name"] == new_phase_name), self.phases[0])
            self.phase_timer = random.uniform(*self.current_phase["duration"])

        execute_behavior(self.current_phase["behavior"], self, game_state, self)

        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY", 0), transparent_bg=True)
