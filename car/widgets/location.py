from textual.widget import Widget
from textual.reactive import reactive

class Location(Widget):
    """A widget to display the player's current location."""

    x = reactive(0)
    y = reactive(0)

    def render(self) -> str:
        """Render the location."""
        return f"Location: ({self.x}, {self.y})"
