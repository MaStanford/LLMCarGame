from textual.screen import ModalScreen
from textual.binding import Binding
from ..widgets.map_view import MapView
import time

# Brief cooldown after mounting to ignore key repeats from the press that opened this screen
_MOUNT_COOLDOWN = 0.25

class MapScreen(ModalScreen):
    """The map screen."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back", show=True),
        Binding("m", "toggle_city_mode", "City/World", show=True),
        Binding("up", "scroll_map(0, -1)", "Scroll", show=False),
        Binding("down", "scroll_map(0, 1)", "Scroll", show=False),
        Binding("left", "scroll_map(-1, 0)", "Scroll", show=False),
        Binding("right", "scroll_map(1, 0)", "Scroll", show=False),
        Binding("w", "nav_node(0, -1)", "Up", show=True),
        Binding("s", "nav_node(0, 1)", "Down", show=True),
        Binding("a", "nav_node(-1, 0)", "Left", show=True),
        Binding("d", "nav_node(1, 0)", "Right", show=True),
        Binding("c", "center_map", "Center", show=True),
        Binding("enter", "select_waypoint", "Waypoint", show=True),
    ]

    def compose(self):
        """Compose the layout of the screen."""
        yield MapView(game_state=self.app.game_state, world=self.app.world)

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self._mount_time = time.time()
        self.query_one(MapView).focus()

    def _past_cooldown(self) -> bool:
        """Check if enough time has passed since mount to accept input."""
        return time.time() - self._mount_time >= _MOUNT_COOLDOWN

    def action_scroll_map(self, dx: int, dy: int) -> None:
        """Scroll the map."""
        if not self._past_cooldown():
            return
        self.query_one(MapView).move_camera(dx, dy)

    def action_nav_node(self, dx: int, dy: int) -> None:
        """Navigate to the nearest node in the given direction."""
        if not self._past_cooldown():
            return
        self.query_one(MapView).nav_to_nearest_node(dx, dy)

    def action_center_map(self) -> None:
        """Center the map on the player."""
        self.query_one(MapView).center_on_player()

    def action_toggle_city_mode(self) -> None:
        """Toggle between world map and city map."""
        if not self._past_cooldown():
            return
        self.query_one(MapView).toggle_city_mode()

    def action_select_waypoint(self) -> None:
        """Set a waypoint to the selected city."""
        self.query_one(MapView).select_waypoint()
        self.app.pop_screen()

    def on_unmount(self) -> None:
        """Called when the screen is unmounted."""
        self.app.start_game_loop()
