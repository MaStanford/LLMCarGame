from textual.widgets import Static
from ..world.generation import get_city_faction
from ..logic.data_loader import FACTION_DATA

class HudLocation(Static):
    """A widget to display the player's current location and faction territory."""

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_timer = self.set_interval(1, self.update_location)

    def update_location(self) -> None:
        """Update the displayed location."""
        if not self.app.game_state:
            return
            
        gs = self.app.game_state
        faction_id = get_city_faction(gs.car_world_x, gs.car_world_y)
        faction_name = FACTION_DATA.get(faction_id, {}).get("name", "The Wasteland")
        
        self.update(f"Location: [bold]{faction_name}[/bold]")