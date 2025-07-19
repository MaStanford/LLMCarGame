from textual.widgets import Static
from textual.reactive import reactive

class CompassHUD(Static):
    can_focus = False
    """A widget to display the direction to a target."""

    target_angle = reactive(0.0)
    player_angle = reactive(0.0)

    def watch_target_angle(self, value: float) -> None:
        self.update_compass()

    def watch_player_angle(self, value: float) -> None:
        self.update_compass()

    def update_compass(self) -> None:
        """Update the compass text."""
        if self.target_angle == 0 and self.player_angle == 0:
            self.update(" ○\n/|\\\n ○")
            return

        angle_diff = (self.target_angle - self.player_angle + 180) % 360 - 180
        
        if abs(angle_diff) < 10:
            arrow = "↑"
        elif angle_diff > 0:
            arrow = "→"
        else:
            arrow = "←"
            
        self.update(f"Quest: {arrow}")

