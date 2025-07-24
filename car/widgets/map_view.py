from textual.widget import Widget
from rich.text import Text
from rich.style import Style
from ..data.game_constants import CITY_SPACING, ROAD_WIDTH
from ..world.generation import get_city_name

class MapView(Widget):
    """A widget to display the world map."""
    can_focus = True

    def __init__(self, game_state, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_state = game_state
        self.cursor_x = 0
        self.cursor_y = 0
        self.cached_map = None
        self.cached_styles = None

    def on_mount(self) -> None:
        """Called when the widget is mounted."""
        self.cursor_x = self.size.width // 2
        self.cursor_y = self.size.height // 2

    def move_cursor(self, dx: int, dy: int):
        """Move the cursor."""
        self.cursor_x = max(0, min(self.size.width - 1, self.cursor_x + dx))
        self.cursor_y = max(0, min(self.size.height - 1, self.cursor_y + dy))
        self.refresh()

    def select_waypoint(self):
        """Set a waypoint to the selected city."""
        gs = self.game_state
        scale = 200
        map_start_x = gs.car_world_x - (self.size.width / 2) * scale
        map_start_y = gs.car_world_y - (self.size.height / 2) * scale
        
        world_x = map_start_x + self.cursor_x * scale
        world_y = map_start_y + self.cursor_y * scale
        
        grid_x = round(world_x / CITY_SPACING)
        grid_y = round(world_y / CITY_SPACING)
        
        if get_city_name(grid_x, grid_y):
            gs.waypoint = (grid_x * CITY_SPACING, grid_y * CITY_SPACING)
            self.app.screen.query_one("#notifications").add_notification(f"Waypoint set to {get_city_name(grid_x, grid_y)}.")

    def _generate_map_cache(self):
        """Generates the static parts of the map and caches them."""
        gs = self.game_state
        w, h = self.size
        scale = 200
        
        map_start_x = gs.car_world_x - (w / 2) * scale
        map_start_y = gs.car_world_y - (h / 2) * scale

        self.cached_map = [[' ' for _ in range(w)] for _ in range(h)]
        self.cached_styles = [[Style() for _ in range(w)] for _ in range(h)]

        for y in range(h):
            for x in range(w):
                world_x = map_start_x + x * scale
                world_y = map_start_y + y * scale
                
                if abs(world_x % CITY_SPACING) < ROAD_WIDTH * scale or abs(world_y % CITY_SPACING) < ROAD_WIDTH * scale:
                    self.cached_map[y][x] = "+"
                    self.cached_styles[y][x] = Style(color="bright_black")
                
                grid_x = round(world_x / CITY_SPACING)
                grid_y = round(world_y / CITY_SPACING)
                if get_city_name(grid_x, grid_y):
                    city_center_x = grid_x * CITY_SPACING
                    city_center_y = grid_y * CITY_SPACING
                    if abs(world_x - city_center_x) < 10 * scale and abs(world_y - city_center_y) < 10 * scale:
                        self.cached_map[y][x] = "C"
                        self.cached_styles[y][x] = Style(color="cyan", bold=True)

    def render(self) -> Text:
        """Render the map."""
        if self.cached_map is None:
            self._generate_map_cache()

        # Start with a copy of the cached map
        canvas = [row[:] for row in self.cached_map]
        styles = [row[:] for row in self.cached_styles]
        
        gs = self.game_state
        w, h = self.size
        scale = 200
        map_start_x = gs.car_world_x - (w / 2) * scale
        map_start_y = gs.car_world_y - (h / 2) * scale

        # Draw Player
        player_x = int((gs.car_world_x - map_start_x) / scale)
        player_y = int((gs.car_world_y - map_start_y) / scale)
        if 0 <= player_y < h and 0 <= player_x < w:
            canvas[player_y][player_x] = "@"
            styles[player_y][player_x] = Style(color="red", bold=True)
            
        # Draw Quest Objective
        if gs.current_quest and gs.current_quest.boss:
            boss = gs.current_quest.boss
            boss_x = int((boss.x - map_start_x) / scale)
            boss_y = int((boss.y - map_start_y) / scale)
            if 0 <= boss_y < h and 0 <= boss_x < w:
                canvas[boss_y][boss_x] = "X"
                styles[boss_y][boss_x] = Style(color="magenta", bold=True)

        # Draw Cursor
        canvas[self.cursor_y][self.cursor_x] = "X"
        styles[self.cursor_y][self.cursor_x] = Style(color="yellow", bold=True)

        # Convert to Rich Text
        text = Text()
        for y, row in enumerate(canvas):
            for x, char in enumerate(row):
                text.append(char, styles[y][x])
            text.append("\n")
        return text
