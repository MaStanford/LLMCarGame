from textual.widgets import Static
from textual.reactive import reactive

class QuestHUD(Static):
    """A widget to display quest information."""

    quest_name = reactive("")

    def on_mount(self) -> None:
        """Called when the widget is mounted."""
        self.update_quest()

    def watch_quest_name(self, value: str) -> None:
        """Called when the quest_name attribute changes."""
        self.update_quest()

    def update_quest(self) -> None:
        """Update the quest display."""
        self.update(f"Quest: {self.quest_name}")
