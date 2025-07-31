from textual.widget import Widget
from rich.text import Text
from rich.style import Style
from ..data.game_constants import CITY_SPACING
from ..world.generation import does_city_exist_at
import time
import random

class MapView(Widget):
    """A widget to display the world map."""
    can_focus = True

    def __init__(self, game_state, world, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_state = game_state
        self.world = world
        self.camera_x = 0
        self.camera_y = 0
        self.map_data = {}
        self.blink_state = True

    def on_mount(self) -> None:
        """Called when the widget is mounted."""
        self.camera_x = self.game_state.car_world_x
        self.camera_y = self.game_state.car_world_y
        self._generate_map_chunk()
        self.blink_timer = self.set_interval(0.5, self.toggle_blink)

    def on_unmount(self) -> None:
        """Called when the widget is unmounted."""
        self.blink_timer.stop()

    def toggle_blink(self) -> None:
        """Toggle the blink state for the player marker."""
        self.blink_state = not self.blink_state
        self.refresh()

    def move_camera(self, dx: int, dy: int):
        """Move the camera."""
        self.camera_x += dx * 200 # Scale factor for scrolling
        self.camera_y += dy * 200
        self.refresh()

    def center_on_player(self):
        """Re-center the map on the player."""
        self.camera_x = self.game_state.car_world_x
        self.camera_y = self.game_state.car_world_y
        self.refresh()

    def _generate_map_chunk(self):
        """Generates a large chunk of the map around the player."""
        gs = self.game_state
        chunk_size = 100000 # World units for the chunk
        
        center_grid_x = round(self.camera_x / CITY_SPACING)
        center_grid_y = round(self.camera_y / CITY_SPACING)
        
        grid_radius = int((chunk_size / 2) / CITY_SPACING)

        for gx in range(center_grid_x - grid_radius, center_grid_x + grid_radius):
            for gy in range(center_grid_y - grid_radius, center_grid_y + grid_radius):
                if does_city_exist_at(gx, gy, self.world.seed, gs.factions):
                    is_hub = any(faction.get("hub_city_coordinates") == [gx, gy] for faction in gs.factions.values())
                    
                    # Add jitter to the city position
                    local_random = random.Random(f"{self.world.seed}-{gx}-{gy}")
                    jitter_x = local_random.uniform(-0.3, 0.3)
                    jitter_y = local_random.uniform(-0.3, 0.3)
                    
                    self.map_data[(gx + jitter_x, gy + jitter_y)] = "★" if is_hub else "■"

    def render(self) -> Text:
        """Render the map."""
        w, h = self.size
        if self.cached_map is None or len(self.cached_map) != h or len(self.cached_map[0]) != w:
            self._generate_map_chunk()

        canvas = [row[:] for row in self.cached_map]
        styles = [row[:] for row in self.cached_styles]
        
        gs = self.game_state
        scale = 200
        map_start_x = self.camera_x - (w / 2) * scale
        map_start_y = self.camera_y - (h / 2) * scale

        # Draw Cities and Labels
        for (gx, gy), symbol in self.map_data.items():
            city_world_x = gx * CITY_SPACING
            city_world_y = gy * CITY_SPACING
            
            sx = int((city_world_x - map_start_x) / scale)
            sy = int((city_world_y - map_start_y) / scale)
            
            if 0 <= sy < h and 0 <= sx < w:
                canvas[sy][sx] = symbol
                styles[sy][sx] = Style(color="cyan", bold=True, bgcolor="black")
                
                city_name = get_city_name(round(gx), round(gy), gs.factions)
                label = f"{city_name} ({int(city_world_x)}, {int(city_world_y)})"
                self._draw_text(canvas, styles, sx + 2, sy, label, Style(color="white", bgcolor="black"))

        # Draw Player
        player_x = int((self.game_state.car_world_x - map_start_x) / scale)
        player_y = int((self.game_state.car_world_y - map_start_y) / scale)
        if 0 <= player_y < h and 0 <= player_x < w:
            if self.blink_state:
                canvas[player_y][player_x] = "●"
                styles[player_y][player_x] = Style(color="red", bold=True, bgcolor="black")
            
        # Convert to Rich Text
        text = Text()
        for y, row in enumerate(canvas):
            for x, char in enumerate(row):
                text.append(char, styles[y][x])
            text.append("\n")
        return text

    def _draw_text(self, canvas, styles, x, y, text, style):
        """Draws text onto the canvas."""
        for i, char in enumerate(text):
            if 0 <= y < len(canvas) and 0 <= x + i < len(canvas[0]):
                canvas[y][x + i] = char
                styles[y][x + i] = style
