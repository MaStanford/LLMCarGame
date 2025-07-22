from textual.screen import ModalScreen
from textual.binding import Binding
from ..widgets.map_view import MapView

class MapScreen(ModalScreen):
    """The map screen."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("m", "app.pop_screen", "Back"),
        Binding("up", "move_cursor(0, -1)", "Up"),
        Binding("down", "move_cursor(0, 1)", "Down"),
        Binding("left", "move_cursor(-1, 0)", "Left"),
        Binding("right", "move_cursor(1, 0)", "Right"),
        Binding("enter", "select_waypoint", "Select"),
    ]

    def compose(self):
        """Compose the layout of the screen."""
        yield MapView(game_state=self.app.game_state)

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.query_one(MapView).focus()

    def action_move_cursor(self, dx: int, dy: int) -> None:
        """Move the map cursor."""
        self.query_one(MapView).move_cursor(dx, dy)

    def action_select_waypoint(self) -> None:
        """Set a waypoint to the selected city."""
        self.query_one(MapView).select_waypoint()
        self.app.pop_screen()
