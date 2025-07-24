import random
from ..vehicle import Vehicle
from ...logic.ai_behaviors import _execute_chase_behavior, _execute_strafe_behavior

class Technical(Vehicle):
    """
    A versatile, gun-mounted pickup used by the Salvage Core.
    It balances direct pursuit with suppressive fire from a distance.
    """
    def __init__(self, x, y):
        art = [
            "  ▄▄▄    ",
            " █ ▆ █═╦╗",
            " (●)═(●) "
        ]
        super().__init__(x, y, art, durability=70, speed=0.7, acceleration=0.5, handling=0.6)
        self.name = "Technical"
        self.xp_value = 25
        self.cash_value = 40
        self.drop_item = "ammo_bullet"
        self.drop_rate = 0.25
        self.phases = [
            {"name": "Approach", "duration": (5, 8), "behavior": "CHASE", "next_phases": {"SuppressiveFire": 1.0}},
            {"name": "SuppressiveFire", "duration": (4, 6), "behavior": "STRAFE", "next_phases": {"Approach": 1.0}}
        ]
        self._initialize_ai()

    def _initialize_ai(self):
        self.current_phase = self.phases[0]
        self.phase_timer = random.uniform(*self.current_phase["duration"])

    def update(self, game_state, world):
        self.phase_timer -= 1 / 30.0

        if self.phase_timer <= 0:
            next_phase_name = list(self.current_phase["next_phases"].keys())[0]
            self.current_phase = next((p for p in self.phases if p["name"] == next_phase_name), self.phases[0])
            self.phase_timer = random.uniform(*self.current_phase["duration"])

        behavior = self.current_phase["behavior"]
        if behavior == "CHASE":
            _execute_chase_behavior(self, game_state, self)
        elif behavior == "STRAFE":
            _execute_strafe_behavior(self, game_state, self)
        
        self.x += self.vx
        self.y += self.vy

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY_SALVAGE", 0), transparent_bg=True)
