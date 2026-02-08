from textual.widgets import Static
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel

class QuestHUD(Static):
    can_focus = False
    """A widget to display quest information."""

    quest_name = reactive("")

    def render(self) -> Panel:
        """Render the quest display."""
        if self.quest_name and self.quest_name != "None":
            content = Text.from_markup(f"[bold]{self.quest_name}[/bold]", justify="center")
            return Panel(content, title="Quest", border_style="white")
        return Panel(Text("No active quest", justify="center", style="dim"), title="Quest", border_style="dim white")

