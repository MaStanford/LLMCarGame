from textual.widgets import Static
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel

class QuestHUD(Static):
    can_focus = False
    """A widget to display quest information."""

    quest_names = reactive([])
    selected_index = reactive(0)

    def render(self) -> Panel:
        """Render the quest display."""
        if self.quest_names:
            content = Text(justify="center")
            for i, name in enumerate(self.quest_names):
                if i == self.selected_index:
                    content.append(f"> {name}", style="bold")
                else:
                    content.append(f"  {name}", style="dim")
                if i < len(self.quest_names) - 1:
                    content.append("\n")
            return Panel(content, title=f"Quests ({len(self.quest_names)}/3)", border_style="white", expand=True)
        return Panel(Text("No active quests", justify="center", style="dim"), title="Quests", border_style="dim white", expand=True)
