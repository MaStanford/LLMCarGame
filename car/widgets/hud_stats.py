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
    ammo = reactive(0)
    max_ammo = reactive(0)

    def on_mount(self) -> None:
        """Called when the widget is mounted."""
        self.update_hud()

    def compose(self):
        with Horizontal(classes="hud-container"):
            with Vertical(classes="hud-column"):
                yield Static(id="cash")
                yield Static(id="durability_label")
                yield ProgressBar(id="durability", total=100, show_eta=False)
                yield Static(id="gas_label")
                yield ProgressBar(id="gas", total=100, show_eta=False)
                yield Static(id="ammo_label")
            with Vertical(classes="hud-column"):
                yield Static(id="xp_label")
                yield ProgressBar(id="xp", total=100, show_eta=False)
                yield Static("Pedal")
                yield ProgressBar(id="pedal", total=200, show_eta=False)
                yield Static(id="speed")
                yield Static(id="level")

    def watch_cash(self, value: int) -> None: self.update_hud()
    def watch_durability(self, value: int) -> None: self.update_hud()
    def watch_max_durability(self, value: int) -> None: self.update_hud()
    def watch_gas(self, value: float) -> None: self.update_hud()
    def watch_gas_capacity(self, value: int) -> None: self.update_hud()
    def watch_speed(self, value: float) -> None: self.update_hud()
    def watch_level(self, value: int) -> None: self.update_hud()
    def watch_xp(self, value: int) -> None: self.update_hud()
    def watch_xp_to_next_level(self, value: int) -> None: self.update_hud()
    def watch_pedal_position(self, value: float) -> None: self.update_hud()
    def watch_ammo(self, value: int) -> None: self.update_hud()
    def watch_max_ammo(self, value: int) -> None: self.update_hud()

    def update_hud(self) -> None:
        """Update all HUD elements."""
        if not self.is_mounted:
            return

        self.query_one("#cash", Static).update(f"Cash: ${self.cash}")
        
        self.query_one("#durability_label", Static).update(f"Durability: {self.durability}/{self.max_durability}")
        durability_bar = self.query_one("#durability", ProgressBar)
        durability_bar.total = self.max_durability
        durability_bar.progress = self.durability
        
        self.query_one("#gas_label", Static).update(f"Gas: {self.gas:.0f}/{self.gas_capacity}")
        gas_bar = self.query_one("#gas", ProgressBar)
        gas_bar.total = self.gas_capacity
        gas_bar.progress = self.gas

        self.query_one("#ammo_label", Static).update(f"Ammo: {self.ammo}/{self.max_ammo}")

        self.query_one("#xp_label", Static).update(f"XP: {self.xp}/{self.xp_to_next_level}")
        xp_bar = self.query_one("#xp", ProgressBar)
        xp_bar.total = self.xp_to_next_level
        xp_bar.progress = self.xp

        pedal_bar = self.query_one("#pedal", ProgressBar)
        pedal_bar.progress = (self.pedal_position + 1.0) * 100

        self.query_one("#speed", Static).update(f"Speed: {abs(self.speed):.1f}")
        self.query_one("#level", Static).update(f"Level: {self.level}")

