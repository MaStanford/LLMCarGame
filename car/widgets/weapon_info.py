from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel

class WeaponInfo(Widget):
    """A widget to display weapon statistics."""

    name = reactive("Weapon")
    damage = reactive(0)
    range = reactive(0)
    fire_rate = reactive(0)

    def render(self) -> Panel:
        """Render the weapon info."""
        content = (
            f"Damage: {self.damage}\n"
            f"Range: {self.range}\n"
            f"Fire Rate: {self.fire_rate}"
        )
        return Panel(Text(content), title=self.name)
