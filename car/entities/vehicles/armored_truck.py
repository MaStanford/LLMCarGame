import random
from ..vehicle import Vehicle
from ...logic.ai_behaviors import _execute_chase_behavior, _execute_ram_behavior, _execute_evade_behavior

class ArmoredTruck(Vehicle):
    """
    A heavily armored security truck. Slow but incredibly durable.
    Its AI is simple and direct: close the distance and crush the target.
    """
    def __init__(self, x, y):
        # New art for a Brinks-style armored truck
        art = [
            "  ▄▄▄▄▄▄▄  ",
            " ▟█▒▒▒▒▒▒█▙ ",
            "███████████",
            "▀(●)▀▀▀(●)▀"
        ]
        # Upgraded stats to match its appearance
        super().__init__(x, y, art, durability=250, speed=4.5, acceleration=0.2, handling=0.05)
        
        # More aggressive AI phases
        self.phases = [
            {"name": "Chase", "duration": (4, 6), "behavior": "CHASE", "next_phases": {"PrepareRam": 1.0}},
            {"name": "PrepareRam", "duration": (1, 2), "behavior": "EVADE", "next_phases": {"Ram": 1.0}},
            {"name": "Ram", "duration": (3, 4), "behavior": "RAM", "next_phases": {"Chase": 1.0}},
        ]
        self._initialize_ai()

    def _initialize_ai(self):
        """Initializes the AI state."""
        self.current_phase = self.phases[0]
        self.phase_timer = random.uniform(self.current_phase["duration"][0], self.current_phase["duration"][1])

    def update(self, game_state, world):
        """Updates the vehicle's state and AI logic each frame."""
        # Countdown the phase timer
        self.phase_timer -= 1 / 30.0 # Assuming 30 FPS

        # Transition to a new phase if the timer runs out
        if self.phase_timer <= 0:
            next_phase_options = list(self.current_phase["next_phases"].keys())
            next_phase_weights = list(self.current_phase["next_phases"].values())
            new_phase_name = random.choices(next_phase_options, weights=next_phase_weights, k=1)[0]
            self.current_phase = next((p for p in self.phases if p["name"] == new_phase_name), self.phases[0])
            self.phase_timer = random.uniform(self.current_phase["duration"][0], self.current_phase["duration"][1])

        # Execute the current AI behavior
        behavior = self.current_phase["behavior"]
        if behavior == "CHASE":
            _execute_chase_behavior(self, game_state, self)
        elif behavior == "RAM":
            _execute_ram_behavior(self, game_state, self)
        elif behavior == "EVADE":
            _execute_evade_behavior(self, game_state, self)
            
        # Update position based on velocity
        self.x += self.vx
        self.y += self.vy

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        """Draws the vehicle on the screen."""
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY", 0), transparent_bg=True)
