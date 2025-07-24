from textual.widgets import Static
from textual.reactive import reactive
from rich.panel import Panel
from rich.text import Text
from rich.progress_bar import ProgressBar
from rich.table import Table
from rich.console import Group
from rich.align import Align

class StatsHUD(Static):
    """A widget to display the player's current stats in the main game view."""

    cash = reactive(0)
    durability = reactive(0)
    max_durability = reactive(100)
    gas = reactive(0.0)
    gas_capacity = reactive(100)
    speed = reactive(0)
    level = reactive(1)
    xp = reactive(0)
    xp_to_next_level = reactive(100)
    ammo = reactive(0)
    max_ammo = reactive(100)
    pedal_position = reactive(0.0)

    def render(self) -> Panel:
        """Render the stats display."""

        top_stats = Text.from_markup(
            f"[b]Cash:[/b] ${self.cash} | [b]Speed:[/b] {int(self.speed)} mph | [b]Level:[/b] {self.level}"
        )

        progress_table = Table.grid(padding=(0, 1), expand=True)
        progress_table.add_column(style="bold", width=4)  # Label
        progress_table.add_column(width=12)  # Bar
        progress_table.add_column(justify="left")  # Value

        progress_table.add_row(
            "DUR:",
            ProgressBar(total=self.max_durability, completed=self.durability, width=10, complete_style="bright_red", finished_style="red"),
            f"{self.durability}/{self.max_durability}"
        )
        progress_table.add_row(
            "GAS:",
            ProgressBar(total=self.gas_capacity, completed=self.gas, width=10, complete_style="bright_green", finished_style="green"),
            f"{int(self.gas)}/{self.gas_capacity}"
        )
        progress_table.add_row(
            "XP:",
            ProgressBar(total=self.xp_to_next_level, completed=self.xp, width=10, complete_style="bright_yellow", finished_style="yellow"),
            f"{self.xp}/{self.xp_to_next_level}"
        )

        pedal_display = ""
        if self.pedal_position > 0:
            pedal_display = f"Accel: [green]{'⬆' * int(self.pedal_position * 5)}[/]"
        elif self.pedal_position < 0:
            pedal_display = f"Brake: [red]{'⬇' * int(abs(self.pedal_position) * 5)}[/]"
        else:
            pedal_display = "     "
            
        bottom_stats = Text.from_markup(
            f"[b]Ammo:[/b] {self.ammo}/{self.max_ammo} | {pedal_display}"
        )

        render_group = Group(
            Align.center(top_stats),
            progress_table,
            Align.center(bottom_stats)
        )

        return Panel(
            render_group,
            title="Stats",
            border_style="white"
        )
