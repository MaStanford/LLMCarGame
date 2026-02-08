from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel
import time

DESTROYED_DISPLAY_DURATION = 1.5


class EntityModal(Widget):
    """A widget to display information about the nearest entity."""
    can_focus = False

    entity_name = reactive("No Target")
    hp = reactive(0)
    max_hp = reactive(0)
    art = reactive([])
    destroyed_name = reactive("")
    destroyed_timer = reactive(0.0)

    def render(self) -> Panel:
        """Render the entity modal."""
        # Check for recent destruction event
        if self.destroyed_name and time.time() - self.destroyed_timer < DESTROYED_DISPLAY_DURATION:
            destroyed_art = (
                "╔═══════════╗\n"
                "║ DESTROYED ║\n"
                "╚═══════════╝"
            )
            return Panel(
                Text(destroyed_art, justify="center", style="bold red"),
                title=self.destroyed_name,
                border_style="bold red",
            )

        if self.max_hp <= 0:
            # Idle state — no entity in range
            idle_art = (
                "┌─────────┐\n"
                "│  ◎ SCAN │\n"
                "└─────────┘"
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
