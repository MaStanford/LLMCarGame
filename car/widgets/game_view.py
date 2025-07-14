from textual.widget import Widget
from rich.text import Text
from rich.style import Style
import math

class GameView(Widget):
    """A widget to display the game world."""
    
    BINDINGS = [
        ("w", "accelerate", "Accelerate"),
        ("s", "brake", "Brake"),
        ("a", "turn_left", "Turn Left"),
        ("d", "turn_right", "Turn Right"),
        ("space", "fire", "Fire"),
        ("escape", "push_screen('pause_menu')", "Pause"),
        ("tab", "push_screen('inventory')", "Inventory")
    ]

    def __init__(self, game_state, world, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_state = game_state
        self.world = world

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
                styles[y][x] = Style.parse(terrain.get("style", ""))

        # Render all entities
        for entity in gs.all_entities:
            self.draw_entity(canvas, styles, entity, world_start_x, world_start_y, w, h)

        # Render particles
        for p_x, p_y, _, _, _, _, particle_char in gs.active_particles:
            sx = int(p_x - world_start_x)
            sy = int(p_y - world_start_y)
            if 0 <= sy < h and 0 <= sx < w:
                canvas[sy][sx] = particle_char
                styles[sy][sx] = Style(color="yellow")

        # Convert canvas to Rich Text
        text = Text()
        for y, row in enumerate(canvas):
            for x, char in enumerate(row):
                text.append(char, styles[y][x])
            text.append("\n")
            
        return text

    def draw_entity(self, canvas, styles, entity, world_start_x, world_start_y, w, h):
        """Draws a single entity on the canvas."""
        if hasattr(entity, 'get_art_for_angle'):
            art = entity.get_art_for_angle(entity.angle)
        elif isinstance(entity.art, dict):
            # Fallback for non-player cars
            art = entity.art.get("N", [""])
        else:
            art = entity.art

        if isinstance(art, str):
            art = art.split('\n')

        art_h = len(art)
        art_w = max(len(line) for line in art) if art else 0
        
        entity_screen_x = int(entity.x - world_start_x - art_w / 2)
        entity_screen_y = int(entity.y - world_start_y - art_h / 2)

        for i, line in enumerate(art):
            for j, char in enumerate(line):
                if char != ' ':
                    y, x = entity_screen_y + i, entity_screen_x + j
                    if 0 <= y < h and 0 <= x < w:
                        canvas[y][x] = char
                        # You can add style logic here if needed
                        # For now, we'll use a default style
                        styles[y][x] = Style(color="white")
