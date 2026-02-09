from textual.widget import Widget
from rich.text import Text
from rich.style import Style
from ..data.game_constants import CITY_SPACING, CITY_SIZE
from ..world.generation import does_city_exist_at, get_buildings_in_city, get_city_name
from ..data.buildings import BUILDING_DATA
import time
import random
import math

# Color mapping for building types on the city map
_BUILDING_STYLES = {
    "mechanic_shop": Style(color="rgb(255,140,0)", bold=True),   # Orange
    "gas_station":   Style(color="rgb(0,200,200)", bold=True),   # Teal
    "weapon_shop":   Style(color="rgb(0,255,0)", bold=True),     # Green
    "city_hall":     Style(color="rgb(255,255,0)", bold=True),   # Yellow
}
_BUILDING_LABELS = {
    "mechanic_shop": "REPAIR",
    "gas_station":   "GAS",
    "weapon_shop":   "AMMO",
    "city_hall":     "HALL",
}
_GENERIC_STYLE = Style(color="rgb(160,160,160)")
_DAMAGED_STYLE = Style(color="rgb(255,165,0)")   # Orange for damaged
_RUBBLE_STYLE = Style(color="rgb(100,100,90)")    # Grey for destroyed


class MapView(Widget):
    """A widget to display the world map or city map."""
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
        self.city_mode = False
        self.city_grid_x = 0
        self.city_grid_y = 0

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

    def toggle_city_mode(self) -> None:
        """Toggle between world map and city map."""
        self.city_mode = not self.city_mode
        if self.city_mode:
            # Snap to the nearest city grid
            self.city_grid_x = round(self.game_state.car_world_x / CITY_SPACING)
            self.city_grid_y = round(self.game_state.car_world_y / CITY_SPACING)
        self.refresh()

    def move_camera(self, dx: int, dy: int):
        """Move the camera."""
        if self.city_mode:
            # In city mode, arrow keys cycle between cities
            self.city_grid_x += dx
            self.city_grid_y += dy
        else:
            self.camera_x += dx * 200
            self.camera_y += dy * 200
        self.refresh()

    def center_on_player(self):
        """Re-center the map on the player."""
        self.camera_x = self.game_state.car_world_x
        self.camera_y = self.game_state.car_world_y
        if self.city_mode:
            self.city_grid_x = round(self.camera_x / CITY_SPACING)
            self.city_grid_y = round(self.camera_y / CITY_SPACING)
        self.refresh()

    def select_waypoint(self):
        """Sets a waypoint to the city closest to the camera's center."""
        if self.city_mode:
            self.game_state.waypoint = {
                "x": self.city_grid_x * CITY_SPACING,
                "y": self.city_grid_y * CITY_SPACING,
                "name": get_city_name(self.city_grid_x, self.city_grid_y, self.game_state.factions),
            }
            return

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
                "name": "Waypoint"
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
        """Render the appropriate map mode."""
        if self.city_mode:
            return self._render_city()
        return self._render_world()

    def _render_city(self) -> Text:
        """Render the city-level map, scaled to fit the screen."""
        w, h = self.size
        gs = self.game_state
        gx, gy = self.city_grid_x, self.city_grid_y

        canvas = [[' ' for _ in range(w)] for _ in range(h)]
        styles = [[Style(bgcolor="rgb(20,20,20)") for _ in range(w)] for _ in range(h)]

        # City bounds in world coordinates
        city_center_x = gx * CITY_SPACING
        city_center_y = gy * CITY_SPACING
        half = CITY_SIZE // 2
        city_min_x = city_center_x - half
        city_min_y = city_center_y - half

        # Leave 2-char margin on each side for labels, 1 row for title
        margin_x = 2
        margin_y = 2
        draw_w = w - margin_x * 2
        draw_h = h - margin_y * 2

        if draw_w <= 0 or draw_h <= 0:
            return Text("Screen too small")

        # Scale: world units per screen character
        scale_x = CITY_SIZE / draw_w
        scale_y = CITY_SIZE / draw_h

        def world_to_screen(wx, wy):
            sx = int((wx - city_min_x) / scale_x) + margin_x
            sy = int((wy - city_min_y) / scale_y) + margin_y
            return sx, sy

        # Draw city ground
        for sy in range(margin_y, margin_y + draw_h):
            for sx in range(margin_x, margin_x + draw_w):
                canvas[sy][sx] = '.'
                styles[sy][sx] = Style(color="rgb(60,60,60)", bgcolor="rgb(20,20,20)")

        # Draw title
        city_name = get_city_name(gx, gy, gs.factions)
        title = f"[ {city_name} ({gx},{gy}) ]"
        title_x = max(0, (w - len(title)) // 2)
        self._draw_text(canvas, styles, title_x, 0, title, Style(color="white", bold=True))

        # Draw mode hint
        hint = "Tab: World Map | Arrows: Next City | C: Center | Enter: Waypoint"
        hint_x = max(0, (w - len(hint)) // 2)
        self._draw_text(canvas, styles, hint_x, h - 1, hint, Style(color="rgb(100,100,100)"))

        # Get buildings
        buildings = get_buildings_in_city(gx, gy)

        for idx, building in enumerate(buildings):
            btype = building.get("type", "GENERIC")
            bld_key = (gx, gy, idx)
            is_destroyed = bld_key in gs.destroyed_buildings

            # Get the label for minimum size calculation
            label = _BUILDING_LABELS.get(btype, building.get("name", "")[:8])
            # Minimum screen size: width = label + 2 (borders), height = 3 (border + label + border)
            # For damaged buildings with HP bar, need height 4
            min_w = len(label) + 2 if label else 3
            min_h = 4

            # Building screen rect
            bx1, by1 = world_to_screen(building['x'], building['y'])
            bx2, by2 = world_to_screen(building['x'] + building['w'], building['y'] + building['h'])

            # Enforce minimum screen size, expanding from center
            actual_w = bx2 - bx1
            actual_h = by2 - by1
            if actual_w < min_w:
                mid_x = (bx1 + bx2) // 2
                bx1 = mid_x - min_w // 2
                bx2 = bx1 + min_w
            if actual_h < min_h:
                mid_y = (by1 + by2) // 2
                by1 = mid_y - min_h // 2
                by2 = by1 + min_h

            # Clamp to drawable area
            bx1 = max(margin_x, min(bx1, margin_x + draw_w - 1))
            by1 = max(margin_y, min(by1, margin_y + draw_h - 1))
            bx2 = max(margin_x + 1, min(bx2, margin_x + draw_w))
            by2 = max(margin_y + 1, min(by2, margin_y + draw_h))

            if bx2 <= bx1 or by2 <= by1:
                continue

            if is_destroyed:
                # Draw rubble
                for sy in range(by1, by2):
                    for sx in range(bx1, bx2):
                        canvas[sy][sx] = '~'
                        styles[sy][sx] = _RUBBLE_STYLE
                # Label
                label = "RUBBLE"
                lx = bx1 + max(0, (bx2 - bx1 - len(label)) // 2)
                ly = by1 + (by2 - by1) // 2
                self._draw_text(canvas, styles, lx, ly, label, _RUBBLE_STYLE)
                continue

            # Check damage state
            is_damaged = bld_key in gs.damaged_buildings
            if is_damaged:
                max_hp = BUILDING_DATA.get(btype, {}).get("base_durability", 200)
                current_hp = gs.damaged_buildings[bld_key]
                hp_pct = current_hp / max_hp if max_hp > 0 else 1.0
            else:
                hp_pct = 1.0

            # Choose style based on type and damage
            if btype in _BUILDING_STYLES and hp_pct > 0.5:
                fill_style = _BUILDING_STYLES[btype]
            elif hp_pct <= 0.5:
                fill_style = _DAMAGED_STYLE
            else:
                fill_style = _GENERIC_STYLE

            # Draw building outline
            for sy in range(by1, by2):
                for sx in range(bx1, bx2):
                    if sy == by1 or sy == by2 - 1 or sx == bx1 or sx == bx2 - 1:
                        # Border
                        if sy == by1 and sx == bx1:
                            canvas[sy][sx] = '┌'
                        elif sy == by1 and sx == bx2 - 1:
                            canvas[sy][sx] = '┐'
                        elif sy == by2 - 1 and sx == bx1:
                            canvas[sy][sx] = '└'
                        elif sy == by2 - 1 and sx == bx2 - 1:
                            canvas[sy][sx] = '┘'
                        elif sy == by1 or sy == by2 - 1:
                            canvas[sy][sx] = '─'
                        else:
                            canvas[sy][sx] = '│'
                        styles[sy][sx] = fill_style
                    else:
                        # Interior
                        canvas[sy][sx] = '░'
                        styles[sy][sx] = Style(color=fill_style.color, dim=True)

            # Draw label inside the building
            interior_w = bx2 - bx1 - 2
            if interior_w >= len(label) and by2 - by1 > 2:
                lx = bx1 + 1 + max(0, (interior_w - len(label)) // 2)
                ly = by1 + (by2 - by1) // 2
                self._draw_text(canvas, styles, lx, ly, label, Style(color="white", bold=True))

            # Show HP bar for damaged buildings
            if is_damaged and by2 - by1 > 3 and interior_w >= 3:
                bar_w = min(interior_w, 8)
                filled = max(1, int(hp_pct * bar_w))
                bar = '█' * filled + '░' * (bar_w - filled)
                bar_x = bx1 + 1 + max(0, (interior_w - bar_w) // 2)
                bar_y = by1 + (by2 - by1) // 2 + 1
                if bar_y < by2 - 1:
                    bar_color = "green" if hp_pct > 0.5 else "yellow" if hp_pct > 0.25 else "red"
                    self._draw_text(canvas, styles, bar_x, bar_y, bar, Style(color=bar_color))

        # Draw player position
        px, py = world_to_screen(gs.car_world_x, gs.car_world_y)
        if 0 <= py < h and 0 <= px < w:
            if self.blink_state:
                canvas[py][px] = '●'
                styles[py][px] = Style(color="red", bold=True)

        # Convert to Rich Text
        text = Text()
        for y, row in enumerate(canvas):
            for x, char in enumerate(row):
                text.append(char, styles[y][x])
            if y < h - 1:
                text.append("\n")
        return text

    def _render_world(self) -> Text:
        """Render the world-level map."""
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

        # Mode hint
        hint = "Tab: City Map"
        self._draw_text(canvas, styles, w - len(hint) - 1, h - 1, hint, Style(color="rgb(100,100,100)"))

        # Convert to Rich Text
        text = Text()
        for y, row in enumerate(canvas):
            for x, char in enumerate(row):
                text.append(char, styles[y][x])
            if y < h - 1:
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
