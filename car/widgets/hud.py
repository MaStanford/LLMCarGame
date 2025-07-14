from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text

class HUD(Widget):
    """A widget to display game statistics."""

    cash = reactive(0)
    durability = reactive(0)
    max_durability = reactive(100)
    gas = reactive(0.0)
    gas_capacity = reactive(100)
    speed = reactive(0.0)

    def render(self) -> Text:
        """Render the HUD."""
        return Text(
            f"Cash: ${self.cash} | Dur: {self.durability}/{self.max_durability} | "
            f"Gas: {self.gas:.0f}/{self.gas_capacity} | Speed: {self.speed:.1f}",
            justify="right"
        )
