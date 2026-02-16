import random
from ..vehicle import Vehicle
from ...logic.ai_behaviors import execute_behavior

from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

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
        super().__init__(x, y, art, durability=300, speed=3.0 * GLOBAL_SPEED_MULTIPLIER, acceleration=0.2, handling=0.03)
        self.name = "War Rig"
        self.is_major_enemy = True
        self.xp_value = 200
        self.cash_value = 300
        self.drop_item = "repair_kit"
        self.drop_rate = 1.0  # Always drops a repair kit
        self.collision_damage = 15
        self.shoot_damage = 5
        self.phases = [
            {"name": "Advance", "duration": (8, 10), "behavior": "CHASE", "next_phases": {"Shoot": 0.6, "DeployMines": 0.4}},
            {"name": "Shoot", "duration": (4, 6), "behavior": "SHOOT", "next_phases": {"DeployMines": 0.5, "Advance": 0.5}},
            {"name": "DeployMines", "duration": (2, 3), "behavior": "DEPLOY_MINE", "next_phases": {"Advance": 1.0}},
            {"name": "Evade", "duration": (4, 5), "behavior": "EVADE", "next_phases": {"Advance": 1.0}}
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
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY_DUSTWIND", 0), transparent_bg=True)
