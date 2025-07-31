from textual.widgets import Static
from ..world.generation import get_city_faction

class HudLocation(Static):
    """A widget to display the player's current location and faction territory."""

    def render(self) -> str:
        """Render the location display."""
        if not self.app.game_state:
            return "Location: Unknown"
            
        gs = self.app.game_state
        faction_id = get_city_faction(gs.car_world_x, gs.car_world_y, gs.factions)
        faction_name = gs.factions.get(faction_id, {}).get("name", "The Wasteland")
        
        return f"Location: [bold]{faction_name}[/bold] ({int(gs.car_world_x)}, {int(gs.car_world_y)})"