from textual.widgets import Static
from textual.reactive import reactive

class LocationHUD(Static):
    """A widget to display the player's current location."""

    x = reactive(0)
    y = reactive(0)
    city_name = reactive("")

    def watch_x(self, value: int) -> None:
        self.update_location()

    def watch_y(self, value: int) -> None:
        self.update_location()
    
    def watch_city_name(self, value: str) -> None:
        self.update_location()

    def update_location(self) -> None:
        """Update the location text."""
        if self.city_name:
            self.update(f"{self.city_name} ({self.x}, {self.y})")
        else:
            self.update(f"Location: ({self.x}, {self.y})")
