from textual.screen import ModalScreen
from textual.binding import Binding
from ..widgets.map_view import MapView

class MapScreen(ModalScreen):
    """The map screen."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back", show=True),
        Binding("m", "app.pop_screen", "Back", show=True),
        Binding("up", "scroll_map(0, -1)", "Up", show=True),
        Binding("down", "scroll_map(0, 1)", "Down", show=True),
        Binding("left", "scroll_map(-1, 0)", "Left", show=True),
        Binding("right", "scroll_map(1, 0)", "Right", show=True),
        Binding("c", "center_map", "Center", show=True),
        Binding("t", "toggle_city_mode", "City/World", show=True),
        Binding("enter", "select_waypoint", "Select", show=True),
    ]

    def compose(self):
        """Compose the layout of the screen."""
        yield MapView(game_state=self.app.game_state, world=self.app.world)

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.query_one(MapView).focus()

    def action_scroll_map(self, dx: int, dy: int) -> None:
        """Scroll the map."""
        self.query_one(MapView).move_camera(dx, dy)

    def action_center_map(self) -> None:
        """Center the map on the player."""
        self.query_one(MapView).center_on_player()

    def action_toggle_city_mode(self) -> None:
        """Toggle between world map and city map."""
        self.query_one(MapView).toggle_city_mode()

    def action_select_waypoint(self) -> None:
        """Set a waypoint to the selected city."""
        self.query_one(MapView).select_waypoint()
        self.app.pop_screen()

    def on_unmount(self) -> None:
        """Called when the screen is unmounted."""
        self.app.start_game_loop()
