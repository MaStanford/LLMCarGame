from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Vertical
from textual.binding import Binding

class QuestCompleteScreen(ModalScreen):
    """A modal screen to show quest completion details."""

    BINDINGS = [
        Binding("enter", "app.pop_screen", "Continue"),
    ]

    def __init__(self, quest) -> None:
        super().__init__()
        self.quest = quest

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        with Vertical(id="quest_complete_container"):
            yield Static(f"[bold]Quest Complete: {self.quest.name}[/bold]", classes="title")
            yield Static("--- REWARDS ---", classes="header")
            yield Static(f"XP: {self.quest.rewards.get('xp', 0)}")
            yield Static(f"Cash: ${self.quest.rewards.get('cash', 0)}")
            yield Static("--- FACTION CHANGES ---", classes="header")
            # TODO: Add reputation and control changes here
            yield Button("Continue", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the continue button."""
        self.app.pop_screen()
