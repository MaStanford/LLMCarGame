from textual.widgets import Static
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel
from ..world.generation import get_city_faction
from ..data.game_constants import CITY_SPACING, CITY_SIZE

class HudLocation(Static):
    """A widget to display the player's current location and faction territory."""

    def render(self) -> Panel:
        """Render the location display."""
        if not self.app.game_state:
            return Panel(Text("Unknown", justify="center"), title="Location", border_style="white")

        gs = self.app.game_state

        # Check if player is in a named city
        location_name = None
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
                        location_name = city_name
                        break
                except (ValueError, IndexError):
                    continue

        if not location_name:
            faction_id = get_city_faction(gs.car_world_x, gs.car_world_y, gs.factions)
            location_name = gs.factions.get(faction_id, {}).get("name", "The Wasteland")

        coords = f"({int(gs.car_world_x)}, {int(gs.car_world_y)})"
        content = Text.from_markup(f"[bold]{location_name}[/bold]\n{coords}", justify="center")
        return Panel(content, title="Location", border_style="white")