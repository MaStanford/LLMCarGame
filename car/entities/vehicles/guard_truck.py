import random
from ..vehicle import Vehicle
from ...logic.ai_behaviors import execute_behavior

from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

class GuardTruck(Vehicle):
    """
    A slow but sturdy truck used by the Blue Syndicate for defensive purposes.
    It stays put until an enemy gets close, then gives a determined chase.
    """
    def __init__(self, x, y):
        art = [
            "  ▄▄▄▄▄  ",
            " ▟█████▙ ",
            "█████████",
            " (●)═(●) "
        ]
        super().__init__(x, y, art, durability=150, speed=3.75 * GLOBAL_SPEED_MULTIPLIER, acceleration=0.2, handling=0.2)
        self.name = "Guard Truck"
        self.xp_value = 30
        self.cash_value = 50
        self.drop_item = "ammo_bullet"
        self.drop_rate = 0.2
        self.collision_damage = 8
        self.shoot_damage = 3
        self.phases = [
            {"name": "Guard", "duration": (1, 2), "behavior": "STATIONARY", "next_phases": {"Shoot": 1.0}},
            {"name": "Shoot", "duration": (3, 5), "behavior": "SHOOT", "next_phases": {"Chase": 0.6, "Guard": 0.4}},
            {"name": "Chase", "duration": (10, 15), "behavior": "CHASE", "next_phases": {"Guard": 1.0}}
        ]
        self._initialize_ai()
        # Guard trucks only become aggressive if the player is close
        self.aggro_radius = 20

    def _initialize_ai(self):
        self.current_phase = self.phases[0]
        self.phase_timer = random.uniform(*self.current_phase["duration"])

    def update(self, game_state, world, dt):
        self.ai_state["elapsed"] = self.ai_state.get("elapsed", 0) + dt

        self.phase_timer -= dt

        dist_to_player = ((self.x - game_state.car_world_x)**2 + (self.y - game_state.car_world_y)**2)**0.5

        # If player is far away, always stay in Guard mode
        if dist_to_player > self.aggro_radius and self.current_phase["name"] != "Guard":
            self.current_phase = self.phases[0]  # Switch to Guard
            self.phase_timer = random.uniform(*self.current_phase["duration"])

        if self.phase_timer <= 0:
            if self.current_phase["name"] == "Guard" and dist_to_player <= self.aggro_radius:
                # If guarding and player is close, switch to Shoot
                self.current_phase = next((p for p in self.phases if p["name"] == "Shoot"), self.phases[1])
            elif self.current_phase["name"] != "Guard":
                # Use weighted phase transitions
                next_phase_options = list(self.current_phase["next_phases"].keys())
                next_phase_weights = list(self.current_phase["next_phases"].values())
                new_phase_name = random.choices(next_phase_options, weights=next_phase_weights, k=1)[0]
                self.current_phase = next((p for p in self.phases if p["name"] == new_phase_name), self.phases[0])
            else:
                # Guarding and player is far, just reset guard timer
                self.current_phase = self.phases[0]

            self.phase_timer = random.uniform(*self.current_phase["duration"])

        execute_behavior(self.current_phase["behavior"], self, game_state, self)

        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY_BLUE", 0), transparent_bg=True)
