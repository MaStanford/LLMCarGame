from textual.widgets import Static
from ..world.generation import get_city_faction
from ..data.game_constants import CITY_SPACING, CITY_SIZE

class HudLocation(Static):
    """A widget to display the player's current location and faction territory."""

    def render(self) -> str:
        """Render the location display."""
        if not self.app.game_state:
            return "Location: Unknown"
            
        gs = self.app.game_state
        
        # Check if player is in a named city
        if gs.world_details and "cities" in gs.world_details:
            for coords_str, city_name in gs.world_details["cities"].items():
                try:
                    grid_x_str, grid_y_str = coords_str.split(',')
                    grid_x, grid_y = int(grid_x_str), int(grid_y_str)
                    
                    city_world_x = grid_x * CITY_SPACING
                    city_world_y = grid_y * CITY_SPACING
                    
                    half_city = CITY_SIZE / 2
                    if (abs(gs.car_world_x - city_world_x) < half_city and
                        abs(gs.car_world_y - city_world_y) < half_city):
                        return f"Location: [bold]{city_name}[/bold] ({int(gs.car_world_x)}, {int(gs.car_world_y)})"
                except (ValueError, IndexError):
                    continue # Skip malformed coordinate strings

        # Fallback to faction territory
        faction_id = get_city_faction(gs.car_world_x, gs.car_world_y, gs.factions)
        faction_name = gs.factions.get(faction_id, {}).get("name", "The Wasteland")
        
        return f"Location: [bold]{faction_name}[/bold] ({int(gs.car_world_x)}, {int(gs.car_world_y)})"