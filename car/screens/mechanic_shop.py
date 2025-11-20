from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Static, Input, Footer
from textual.containers import Vertical

class MechanicShopScreen(ModalScreen):
    """A modal screen for the mechanic shop."""

    def __init__(self, game_state) -> None:
        self.game_state = game_state
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical(id="mechanic-shop-dialog"):
            yield Static("Mechanic Shop", id="mechanic-shop-title")
            yield Button("Purchase New Attachment Point", id="purchase-attachment")
            yield Button("Upgrade Attachment Point", id="upgrade-attachment")
            yield Button("Back", id="back")
        yield Footer(show_command_palette=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
        # Add logic for purchase/upgrade later
