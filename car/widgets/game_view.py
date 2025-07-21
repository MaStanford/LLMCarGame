from textual.widget import Widget
from textual.events import Key
from ..common.utils import angle_to_direction
from ..data.colors import ATTACHMENT_COLOR_MAP
from ..data.game_constants import CITY_SPACING
from ..world.generation import get_buildings_in_city
from rich.text import Text
from rich.style import Style
import math

class GameView(Widget):
    """A widget to display the game world."""
    can_focus = True
    
    BINDINGS = [
        ("escape", "push_screen('pause_menu')", "Pause"),
        ("tab", "push_screen('inventory')", "Inventory")
    ]

    def __init__(self, game_state, world, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_state = game_state
        self.world = world
        self.active_keys = set()

    def on_key(self, event: Key) -> None:
        """Called when a key is pressed."""
        gs = self.game_state
        
        if event.key == "w":
            gs.pedal_position = min(1.0, gs.pedal_position + 0.2)
        elif event.key == "s":
            gs.pedal_position = max(-1.0, gs.pedal_position - 0.2)
        else:
            self.active_keys.add(event.key)

    def process_input(self) -> None:
        """Process input from the active_keys set for this frame."""
        gs = self.game_state

        # Reset non-pedal actions to False at the start of the frame
        for action in ["turn_left", "turn_right", "fire"]:
            gs.actions[action] = False

        # Set actions to True if their key was pressed this frame
        if "a" in self.active_keys:
            gs.actions["turn_left"] = True
        if "d" in self.active_keys:
            gs.actions["turn_right"] = True
        if "space" in self.active_keys:
            gs.actions["fire"] = True
        
        # Clear the set for the next frame
        self.active_keys.clear()


    def render(self) -> Text:
        """Render the game world."""
        gs = self.game_state
        if not gs:
            return Text("")
            
        w, h = self.size
        world_start_x = gs.car_world_x - w / 2
        world_start_y = gs.car_world_y - h / 2

        canvas = [[' ' for _ in range(w)] for _ in range(h)]
        styles = [[Style() for _ in range(w)] for _ in range(h)]

        # Render terrain
        for y in range(h):
            for x in range(w):
                cwx = int(world_start_x + x)
                cwy = int(world_start_y + y)
                terrain = self.world.get_terrain_at(cwx, cwy)
                canvas[y][x] = terrain.get("char", " ")
                styles[y][x] = terrain.get("style", Style())

        # Render buildings
        city_grid_x = round(gs.car_world_x / CITY_SPACING)
        city_grid_y = round(gs.car_world_y / CITY_SPACING)
        buildings = get_buildings_in_city(city_grid_x, city_grid_y)
        for building in buildings:
            self.draw_building(canvas, styles, building, world_start_x, world_start_y, w, h)

        # Render all entities
        world_end_x = world_start_x + w
        world_end_y = world_start_y + h
        for entity in gs.all_entities:
            # --- Culling Logic ---
            # Skip drawing entities that are off-screen
            if entity is not gs.player_car:
                if (entity.x + entity.width < world_start_x or
                    entity.x - entity.width > world_end_x or
                    entity.y + entity.height < world_start_y or
                    entity.y - entity.height > world_end_y):
                    continue
            
            self.draw_entity(canvas, styles, entity, world_start_x, world_start_y, w, h)

        # Render particles
        for p_x, p_y, _, _, _, _, particle_char, _, _ in gs.active_particles:
            sx = int(p_x - world_start_x)
            sy = int(p_y - world_start_y)
            if 0 <= sy < h and 0 <= sx < w:
                canvas[sy][sx] = particle_char
                styles[sy][sx] = Style(color="yellow")

        # Convert canvas to Rich Text using optimized run-length encoding
        text = Text()
        for y, row in enumerate(canvas):
            if not row:
                text.append("\n")
                continue
            
            current_run = ""
            current_style = styles[y][0]
            
            for x, char in enumerate(row):
                style = styles[y][x]
                if style == current_style:
                    current_run += char
                else:
                    text.append(current_run, current_style)
                    current_run = char
                    current_style = style
            
            text.append(current_run, current_style)
            text.append("\n")
            
        return text

    def draw_entity(self, canvas, styles, entity, world_start_x, world_start_y, w, h):
        """Draws a single entity on the canvas."""
        # Determine the correct art based on the entity's type and angle
        if isinstance(entity.art, dict):
            direction = angle_to_direction(entity.angle)
            art = entity.art.get(direction, entity.art.get("N", ["?"])) # Fallback to North
        elif isinstance(entity.art, list):
            art = entity.art # Use the list directly
        else:
            # Fallback for any other unexpected art type
            art = ["?"]

        if isinstance(art, str):
            art = art.split('\n')

        # Apply color to player car
        entity_style = Style(color="white") # Default style for all entities
        if entity is self.game_state.player_car:
            color_name = self.game_state.car_color_names[0]
            color = color_name.lower().replace("car_", "")
            entity_style = Style(color=color)

        art_h = len(art)
        art_w = max(len(line) for line in art) if art else 0
        
        # Calculate screen position
        if entity is self.game_state.player_car:
            # Center the player car
            entity_screen_x = int(w / 2 - art_w / 2)
            entity_screen_y = int(h / 2 - art_h / 2)
            
            # Draw mounted weapons
            for point_name, weapon in self.game_state.mounted_weapons.items():
                if weapon:
                    point_data = self.game_state.attachment_points.get(point_name)
                    if point_data:
                        self.draw_weapon(canvas, styles, entity, weapon, point_data, world_start_x, world_start_y, w, h)

        else:
            # Position other entities relative to the player
            entity_screen_x = int(entity.x - world_start_x - art_w / 2)
            entity_screen_y = int(entity.y - world_start_y - art_h / 2)

        # Draw the entity's main art on the canvas
        for i, line in enumerate(art):
            for j, char in enumerate(line):
                if char != ' ':
                    y, x = entity_screen_y + i, entity_screen_x + j
                    if 0 <= y < h and 0 <= x < w:
                        canvas[y][x] = char
                        styles[y][x] = entity_style

    def draw_building(self, canvas, styles, building, world_start_x, world_start_y, w, h):
        """Draws a single building on the canvas."""
        b_x, b_y, b_w, b_h = building["x"], building["y"], building["w"], building["h"]
        b_type = building.get("type", "GENERIC")

        # Calculate screen position
        start_sx = int(b_x - world_start_x)
        start_sy = int(b_y - world_start_y)

        # Get the base style for the building type
        building_style = Style(bgcolor="rgb(80,80,80)") # Default for generic
        if b_type != "GENERIC":
            color_name = self.world.building_data[b_type].get("color_pair_name", "BUILDING_WALL")
            building_style = self.world.terrain_data[color_name]["style"]

        if b_type != "GENERIC" and b_type in self.world.building_data:
            art = self.world.building_data[b_type].get("art", [])
            for i, line in enumerate(art):
                for j, char in enumerate(line):
                    if char != ' ':
                        sx, sy = start_sx + j, start_sy + i
                        if 0 <= sy < h and 0 <= sx < w:
                            canvas[sy][sx] = char
                            styles[sy][sx] = building_style
        else:
            # Fallback to procedural drawing for GENERIC buildings
            end_sx = start_sx + b_w
            end_sy = start_sy + b_h
            wall_style = self.world.terrain_data["BUILDING_WALL"]["style"]
            fill_style = Style(bgcolor="rgb(50,50,50)") # Darker fill for generic
            for sy in range(start_sy, end_sy):
                for sx in range(start_sx, end_sx):
                    if 0 <= sy < h and 0 <= sx < w:
                        char = " "
                        style = fill_style
                        # Edges
                        if sy == start_sy or sy == end_sy - 1 or sx == start_sx or sx == end_sx - 1:
                             char = " "
                             style = wall_style
                        
                        canvas[sy][sx] = char
                        styles[sy][sx] = style

    def draw_weapon(self, canvas, styles, parent_entity, weapon, point_data, world_start_x, world_start_y, w, h):
        """Draws a weapon on the canvas at its attachment point."""
        direction = angle_to_direction(parent_entity.angle)
        art = weapon.art.get(direction, weapon.art.get("N", ["|"])) # Fallback to North

        if isinstance(art, str):
            art = art.split('\n')

        art_h = len(art)
        art_w = max(len(line) for line in art) if art else 0

        # --- Rotation Logic (mirrors weapon_systems.py) ---
        adjusted_angle = parent_entity.angle
        car_cos = math.cos(adjusted_angle)
        car_sin = math.sin(adjusted_angle)
        
        offset_x = point_data["offset_x"]
        offset_y = point_data["offset_y"]
        
        rotated_offset_x = offset_x * car_cos - offset_y * car_sin
        rotated_offset_y = offset_x * car_sin + offset_y * car_cos
        
        # Final weapon position in world coordinates
        weapon_world_x = self.game_state.car_world_x + rotated_offset_x
        weapon_world_y = self.game_state.car_world_y + rotated_offset_y

        # Convert world coords to screen coords
        weapon_screen_x = int(weapon_world_x - world_start_x - art_w / 2)
        weapon_screen_y = int(weapon_world_y - world_start_y - art_h / 2)

        # Determine weapon color
        car_color_name = self.game_state.car_color_names[0]
        attachment_color = ATTACHMENT_COLOR_MAP.get(car_color_name, "white")
        weapon_style = Style(color=attachment_color)

        # Draw the weapon art
        for i, line in enumerate(art):
            for j, char in enumerate(line):
                if char != ' ':
                    y, x = weapon_screen_y + i, weapon_screen_x + j
                    if 0 <= y < h and 0 <= x < w:
                        canvas[y][x] = char
                        styles[y][x] = weapon_style