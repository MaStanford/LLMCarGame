from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Container
from textual.binding import Binding

class NarrativeDialogScreen(ModalScreen):
    """A screen to display narrative text from a discovered item."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back", show=True),
    ]

    def __init__(self, narrative_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.narrative_data = narrative_data

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        with Container(id="narrative-dialog-container"):
            yield Static(self.narrative_data.get("title", "A Discovery"), id="narrative_title", classes="panel-title")
            yield Static(self.narrative_data.get("text", ""), id="narrative_text")
            yield Button("Continue", id="continue_button", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "continue_button":
            self.handle_action()
            self.app.pop_screen()

    def handle_action(self):
        """Performs the action associated with the narrative item."""
        action = self.narrative_data.get("action")
        if action == "waypoint":
            self.app.game_state.waypoint = {
                "x": self.narrative_data.get("target_x", 0),
                "y": self.narrative_data.get("target_y", 0),
                "name": self.narrative_data.get("title", "Waypoint")
            }
            for screen in self.app.screen_stack:
                notifications = screen.query("#notifications")
                if notifications:
                    notifications.first().add_notification("New waypoint set.")
                    break