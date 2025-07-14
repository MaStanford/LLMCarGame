from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel

class EntityModal(Widget):
    """A widget to display information about the nearest entity."""

    name = reactive("No Target")
    hp = reactive(0)
    max_hp = reactive(100)
    art = reactive([])

    def render(self) -> Panel:
        """Render the entity modal."""
        hp_percent = (self.hp / self.max_hp) * 100 if self.max_hp > 0 else 0
        hp_bar_width = 20
        hp_filled = int(hp_bar_width * hp_percent / 100)
        hp_bar = f"HP: [{'█'*hp_filled}{'░'*(hp_bar_width-hp_filled)}]"

        art_str = "\n".join(self.art)
        
        content = f"{hp_bar}\n\n{art_str}"
        
        return Panel(Text(content, justify="center"), title=self.name)
