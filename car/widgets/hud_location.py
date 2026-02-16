from textual.widgets import Static
from rich.text import Text
from rich.panel import Panel


class HudLocation(Static):
    """A widget to display the player's current location and faction territory."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._location_name = "Unknown"
        self._coords = "(0, 0)"

    def update_location(self, location_name: str, x: int, y: int) -> None:
        """Update the location display with new data."""
        self._location_name = location_name
        self._coords = f"({x}, {y})"
        self.refresh()

    def render(self) -> Panel:
        """Render the location display."""
        content = Text.from_markup(
            f"[bold]{self._location_name}[/bold]\n{self._coords}",
            justify="center",
        )
        return Panel(content, title="Location", border_style="white", expand=True)
