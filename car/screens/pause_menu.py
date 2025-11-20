from textual.screen import ModalScreen
from textual.widgets import Button, Footer
from textual.binding import Binding
from ..logic.save_load import save_game
from .main_menu import MainMenuScreen
from .quest_detail import QuestDetailScreen
from .save_game import SaveGameScreen

class PauseScreen(ModalScreen):
    """The pause menu screen."""

    BINDINGS = [
        Binding("up", "focus_previous", "Up"),
        Binding("down", "focus_next", "Down"),
        Binding("escape", "resume_game", "Back"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.focusable_widgets = []
        self.current_focus_index = 0

    def compose(self):
        """Compose the layout of the screen."""
        yield Button("Resume", id="resume", variant="primary")
        yield Button("Quests", id="quests", variant="default")
        yield Button("Save Game", id="save_game", variant="default")
        yield Button("Main Menu", id="main_menu", variant="default")
        yield Button("Quit", id="quit", variant="error")
        yield Footer(show_command_palette=True)

    def on_mount(self) -> None:
        """Set up the focusable widgets."""
        self.focusable_widgets = self.query(Button)
        self.update_focus()

    def update_focus(self) -> None:
        """Update the visual focus state."""
        for i, widget in enumerate(self.focusable_widgets):
            if i == self.current_focus_index:
                widget.add_class("focused")
                widget.focus()
            else:
                widget.remove_class("focused")

    def action_focus_previous(self) -> None:
        """Focus the previous widget."""
        self.current_focus_index = (self.current_focus_index - 1 + len(self.focusable_widgets)) % len(self.focusable_widgets)
        self.update_focus()

    def action_focus_next(self) -> None:
        """Focus the next widget."""
        self.current_focus_index = (self.current_focus_index + 1) % len(self.focusable_widgets)
        self.update_focus()

    def action_resume_game(self) -> None:
        """Resume the game."""
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "resume":
            self.app.pop_screen()
        elif event.button.id == "quests":
            self.app.push_screen(QuestDetailScreen())
        elif event.button.id == "save_game":
            self.app.push_screen(SaveGameScreen())
        elif event.button.id == "main_menu":
            self.app.stop_game_loop()
            self.app.switch_screen(MainMenuScreen())
        elif event.button.id == "quit":
            self.app.exit()

