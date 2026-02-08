from textual.widgets import Static
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel

class CompassHUD(Static):
    """A widget to display the direction to a target and the target's name."""

    target_angle = reactive(0.0)
    player_angle = reactive(0.0)
    target_name = reactive("")

    def watch_target_angle(self, value: float) -> None:
        self.refresh()
    def watch_player_angle(self, value: float) -> None:
        self.refresh()
    def watch_target_name(self, value: str) -> None:
        self.refresh()

    def render(self) -> Panel:
        """Render the compass display."""
        if not self.target_name:
            content = Text("No objective", justify="center", style="dim")
            return Panel(content, title="Compass", border_style="dim white")

        angle_diff = (self.target_angle - self.player_angle + 180) % 360 - 180

        if abs(angle_diff) < 10:
            arrow = "↑"
        elif abs(angle_diff) > 170:
            arrow = "↓"
        elif angle_diff > 0:
            arrow = "→"
        else:
            arrow = "←"

        content = Text.from_markup(
            f"[bold]{arrow}[/bold] {self.target_name}",
            justify="center",
        )
        return Panel(content, title="Compass", border_style="white")

