from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel

class EntityModal(Widget):
    can_focus = False
    """A widget to display information about the nearest entity."""

    entity_name = reactive("No Target")
    hp = reactive(0)
    max_hp = reactive(0)
    art = reactive([])

    def render(self) -> Panel:
        """Render the entity modal."""
        if self.max_hp <= 0:
            # Idle state — no entity in range
            idle_art = (
                "    ╱·····╲\n"
                "   ( scanning )\n"
                "    ╲·····╱"
            )
            return Panel(
                Text(idle_art, justify="center", style="dim"),
                title="No Target",
                border_style="dim white",
            )

        hp_percent = (self.hp / self.max_hp) * 100
        hp_bar_width = 20
        hp_filled = int(hp_bar_width * hp_percent / 100)
        hp_color = "green" if hp_percent > 50 else "yellow" if hp_percent > 25 else "red"
        hp_bar = f"HP: [{hp_color}]{'█'*hp_filled}[/][dim]{'░'*(hp_bar_width-hp_filled)}[/]"

        art_str = "\n".join(self.art) if self.art else ""

        content = f"{hp_bar}\n\n{art_str}" if art_str else hp_bar

        return Panel(Text.from_markup(content, justify="center"), title=self.entity_name, border_style="bold red")

