from textual.widget import Widget
from rich.text import Text
from rich.style import Style
from ..data.game_constants import CITY_SPACING
from ..world.generation import does_city_exist_at
import time
import random
import math

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
        self.cached_map = None
        self.cached_styles = None

    def on_mount(self) -> None:
        """Called when the widget is mounted."""
        self.camera_x = self.game_state.car_world_x
        self.camera_y = self.game_state.car_world_y
        w, h = self.size
        self.cached_map = [[' ' for _ in range(w)] for _ in range(h)]
        self.cached_styles = [[Style() for _ in range(w)] for _ in range(h)]
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
        
    def select_waypoint(self):
        """Sets a waypoint to the city closest to the camera's center."""
        min_dist = float('inf')
        closest_city_coords = None
        
        for (gx, gy), _ in self.map_data.items():
            city_world_x = gx * CITY_SPACING
            city_world_y = gy * CITY_SPACING
            dist = math.sqrt((self.camera_x - city_world_x)**2 + (self.camera_y - city_world_y)**2)
            
            if dist < min_dist:
                min_dist = dist
                closest_city_coords = (city_world_x, city_world_y)
        
        if closest_city_coords:
            self.game_state.waypoint = {
                "x": closest_city_coords[0],
                "y": closest_city_coords[1],
                "name": "Waypoint" # Names could be improved later
            }


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
                    
                    local_random = random.Random(f"{self.world.seed}-{gx}-{gy}")
                    jitter_x = local_random.uniform(-0.3, 0.3)
                    jitter_y = local_random.uniform(-0.3, 0.3)
                    
                    self.map_data[(gx + jitter_x, gy + jitter_y)] = ("★" if is_hub else "■", gx, gy)


    def render(self) -> Text:
        """Render the map."""
        w, h = self.size
        
        canvas = [[' ' for _ in range(w)] for _ in range(h)]
        styles = [[Style(bgcolor="black") for _ in range(w)] for _ in range(h)]
        
        gs = self.game_state
        scale = 200
        map_start_x = self.camera_x - (w / 2) * scale
        map_start_y = self.camera_y - (h / 2) * scale

        # Draw Roads
        if gs.world_details and "roads" in gs.world_details:
            for road in gs.world_details["roads"]:
                try:
                    from_x_str, from_y_str = road["from"].split(',')
                    to_x_str, to_y_str = road["to"].split(',')
                    from_gx, from_gy = int(from_x_str), int(from_y_str)
                    to_gx, to_gy = int(to_x_str), int(to_y_str)

                    from_wx = from_gx * CITY_SPACING
                    from_wy = from_gy * CITY_SPACING
                    to_wx = to_gx * CITY_SPACING
                    to_wy = to_gy * CITY_SPACING

                    sx1 = int((from_wx - map_start_x) / scale)
                    sy1 = int((from_wy - map_start_y) / scale)
                    sx2 = int((to_wx - map_start_x) / scale)
                    sy2 = int((to_wy - map_start_y) / scale)
                    
                    self._draw_line(canvas, styles, sx1, sy1, sx2, sy2, "·", Style(color="yellow"))
                    
                    mid_x = (sx1 + sx2) // 2
                    mid_y = (sy1 + sy2) // 2
                    self._draw_text(canvas, styles, mid_x + 1, mid_y, road.get("name", ""), Style(color="yellow", italic=True))
                except (ValueError, KeyError):
                    continue
        
        # Draw Landmarks
        if gs.world_details and "landmarks" in gs.world_details:
            for landmark in gs.world_details["landmarks"]:
                try:
                    lx, ly = landmark["x"], landmark["y"]
                    sx = int((lx - map_start_x) / scale)
                    sy = int((ly - map_start_y) / scale)
                    
                    if 0 <= sy < h and 0 <= sx < w:
                        canvas[sy][sx] = "◊"
                        styles[sy][sx] = Style(color="magenta", bold=True)
                        self._draw_text(canvas, styles, sx + 2, sy, landmark.get("name", ""), Style(color="magenta"))
                except (ValueError, KeyError):
                    continue


        # Draw Cities and Labels
        for (gx, gy), (symbol, orig_gx, orig_gy) in self.map_data.items():
            city_world_x = gx * CITY_SPACING
            city_world_y = gy * CITY_SPACING
            
            sx = int((city_world_x - map_start_x) / scale)
            sy = int((city_world_y - map_start_y) / scale)
            
            if 0 <= sy < h and 0 <= sx < w:
                canvas[sy][sx] = symbol
                styles[sy][sx] = Style(color="cyan", bold=True)
                
                city_name = gs.world_details.get("cities", {}).get(f"{orig_gx},{orig_gy}", "Unknown City")
                self._draw_text(canvas, styles, sx + 2, sy, city_name, Style(color="white"))

        # Draw Player
        player_x = int((self.game_state.car_world_x - map_start_x) / scale)
        player_y = int((self.game_state.car_world_y - map_start_y) / scale)
        if 0 <= player_y < h and 0 <= player_x < w:
            if self.blink_state:
                canvas[player_y][player_x] = "●"
                styles[player_y][player_x] = Style(color="red", bold=True)
            
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

    def _draw_line(self, canvas, styles, x1, y1, x2, y2, char, style):
        """Draws a line onto the canvas using Bresenham's algorithm."""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            if 0 <= y1 < len(canvas) and 0 <= x1 < len(canvas[0]):
                canvas[y1][x1] = char
                styles[y1][x1] = style
            
            if x1 == x2 and y1 == y2:
                break
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
