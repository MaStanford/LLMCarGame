from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Container
from textual.binding import Binding

class QuestDetailScreen(ModalScreen):
    """A screen to display the details of the current quest."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back", show=True),
    ]

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        with Container(id="quest-detail-container"):
            yield Static(id="quest_title", classes="panel-title")
            yield Static(id="quest_dialog")
            yield Static(id="quest_rewards")
            yield Button("Quit Quest", id="quit_quest", variant="error")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        quest = self.app.game_state.current_quest
        if quest:
            self.query_one("#quest_title", Static).update(quest.name)
            self.query_one("#quest_dialog", Static).update(quest.description)
            
            rewards_str = f"""
            Rewards:
            - XP: {quest.rewards.get("xp", 0)}
            - Cash: ${quest.rewards.get("cash", 0)}
            """
            self.query_one("#quest_rewards", Static).update(rewards_str)
        else:
            self.query_one("#quest_title", Static).update("No Active Quest")
            self.query_one("#quit_quest", Button).disabled = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "quit_quest":
            # (Apply reputation penalty - to be implemented)
            self.app.game_state.current_quest = None
            self.app.screen.query_one("#notifications").add_notification("Quest Abandoned.")
            self.app.pop_screen()