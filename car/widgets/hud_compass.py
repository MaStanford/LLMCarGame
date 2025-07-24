from textual.widgets import Static
from textual.reactive import reactive
from textual.containers import Vertical

class CompassHUD(Static):
    """A widget to display the direction to a target and the target's name."""

    target_angle = reactive(0.0)
    player_angle = reactive(0.0)
    target_name = reactive("")

    def compose(self):
        """Compose the layout of the widget."""
        yield Static(id="compass_arrow")
        yield Static(id="compass_target_name")

    def watch_target_angle(self, value: float) -> None:
        self._update_display()
    def watch_player_angle(self, value: float) -> None:
        self._update_display()
    def watch_target_name(self, value: str) -> None:
        self._update_display()

    def _update_display(self) -> None:
        """Update the compass text and target name."""
        arrow_widget = self.query_one("#compass_arrow", Static)
        target_widget = self.query_one("#compass_target_name", Static)

        if not self.target_name:
            arrow_widget.update(" ○\n/|\\\n ○")
            target_widget.update("")
            return

        angle_diff = (self.target_angle - self.player_angle + 180) % 360 - 180
        
        if abs(angle_diff) < 10:
            arrow = "↑"
        elif angle_diff > 0:
            arrow = "→"
        else:
            arrow = "←"
            
        arrow_widget.update(f"Quest: {arrow}")
        target_widget.update(f"Target: {self.target_name}")

