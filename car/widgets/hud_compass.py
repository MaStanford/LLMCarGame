from textual.widgets import Static
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel

# 8-direction compass using Unicode arrows (absolute bearing, 0=North)
_DIRECTIONS = [
    (  0, "\u2191", "N"),   # ↑
    ( 45, "\u2197", "NE"),  # ↗
    ( 90, "\u2192", "E"),   # →
    (135, "\u2198", "SE"),  # ↘
    (180, "\u2193", "S"),   # ↓
    (225, "\u2199", "SW"),  # ↙
    (270, "\u2190", "W"),   # ←
    (315, "\u2196", "NW"),  # ↖
]

def _bearing_to_arrow(bearing_deg):
    """Convert an absolute bearing (degrees, 0=North) to an arrow and cardinal label."""
    a = bearing_deg % 360
    best = _DIRECTIONS[0]
    best_diff = 360
    for center, arrow, label in _DIRECTIONS:
        diff = min(abs(a - center), 360 - abs(a - center))
        if diff < best_diff:
            best_diff = diff
            best = (center, arrow, label)
    return best[1], best[2]


class CompassHUD(Static):
    """A widget to display the absolute direction to a target."""

    absolute_bearing = reactive(0.0)
    target_name = reactive("")

    def watch_absolute_bearing(self, value: float) -> None:
        self.refresh()
    def watch_target_name(self, value: str) -> None:
        self.refresh()

    def render(self) -> Panel:
        """Render the compass display."""
        if not self.target_name:
            content = Text("No objective", justify="center", style="dim")
            return Panel(content, title="Compass", border_style="dim white")

        arrow, cardinal = _bearing_to_arrow(self.absolute_bearing)

        content = Text.from_markup(
            f"[bold]{arrow}[/bold] {cardinal}  {self.target_name}",
            justify="center",
        )
        return Panel(content, title="Compass", border_style="white")
