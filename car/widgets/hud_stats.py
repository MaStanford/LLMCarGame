from textual.widgets import Static, ProgressBar
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive

class StatsHUD(Static):
    can_focus = False
    """A widget to display game statistics."""

    cash = reactive(0)
    durability = reactive(0)
    max_durability = reactive(100)
    gas = reactive(0.0)
    gas_capacity = reactive(100)
    speed = reactive(0.0)
    level = reactive(1)
    xp = reactive(0)
    xp_to_next_level = reactive(100)
    pedal_position = reactive(0.0)

    def on_mount(self) -> None:
        """Called when the widget is mounted."""
        self.update_hud()

    def compose(self):
        with Horizontal(classes="hud-container"):
            with Vertical(classes="hud-column"):
                yield Static(id="cash")
                yield Static("Durability")
                yield ProgressBar(id="durability", total=100, show_eta=False)
                yield Static("Gas")
                yield ProgressBar(id="gas", total=100, show_eta=False)
            with Vertical(classes="hud-column"):
                yield Static("XP")
                yield ProgressBar(id="xp", total=100, show_eta=False)
                yield Static("Pedal")
                yield ProgressBar(id="pedal", total=200, show_eta=False)
                yield Static(id="speed")
                yield Static(id="level")

    def watch_cash(self, value: int) -> None:
        self.update_hud()

    def watch_durability(self, value: int) -> None:
        self.update_hud()

    def watch_max_durability(self, value: int) -> None:
        self.update_hud()

    def watch_gas(self, value: float) -> None:
        self.update_hud()

    def watch_gas_capacity(self, value: int) -> None:
        self.update_hud()

    def watch_speed(self, value: float) -> None:
        self.update_hud()

    def watch_level(self, value: int) -> None:
        self.update_hud()

    def watch_xp(self, value: int) -> None:
        self.update_hud()

    def watch_xp_to_next_level(self, value: int) -> None:
        self.update_hud()

    def watch_pedal_position(self, value: float) -> None:
        self.update_hud()

    def update_hud(self) -> None:
        """Update all HUD elements."""
        if not self.is_mounted:
            return

        self.query_one("#cash", Static).update(f"Cash: ${self.cash}")
        
        durability_bar = self.query_one("#durability", ProgressBar)
        durability_bar.total = self.max_durability
        durability_bar.progress = self.durability
        
        gas_bar = self.query_one("#gas", ProgressBar)
        gas_bar.total = self.gas_capacity
        gas_bar.progress = self.gas

        xp_bar = self.query_one("#xp", ProgressBar)
        xp_bar.total = self.xp_to_next_level
        xp_bar.progress = self.xp

        pedal_bar = self.query_one("#pedal", ProgressBar)
        pedal_bar.progress = (self.pedal_position + 1.0) * 100 # Map -1 to 1 -> 0 to 200

        self.query_one("#speed", Static).update(f"Speed: {abs(self.speed):.1f}")
        self.query_one("#level", Static).update(f"Level: {self.level}")

