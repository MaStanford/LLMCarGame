from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel
from rich.table import Table


class WeaponHUD(Widget):
    """A widget to display mounted weapons, their type, and ammo in the world screen."""

    can_focus = False

    # Serialized weapon data: list of dicts with keys: mount_name, weapon_name, ammo_type, ammo, empty
    weapons_data = reactive([], always_update=True)

    def render(self) -> Panel:
        """Render the weapons panel."""
        if not self.weapons_data:
            return Panel(Text("No mounts", justify="center", style="dim"), title="Weapons")

        table = Table.grid(padding=(0, 1), expand=True)
        table.add_column(width=10)  # Mount / Weapon name
        table.add_column(width=8)   # Ammo type
        table.add_column(justify="right", width=7)  # Ammo count

        for wp in self.weapons_data:
            if wp["empty"]:
                table.add_row(
                    Text(wp["mount_name"], style="dim"),
                    Text("--", style="dim"),
                    Text("--", style="dim"),
                )
            else:
                ammo_str = str(wp["ammo"])
                ammo_style = "bold red" if wp["ammo"] <= 5 else "bold green" if wp["ammo"] > 50 else "bold yellow"
                table.add_row(
                    Text(wp["weapon_name"], style="bold"),
                    Text(wp["ammo_type"], style="cyan"),
                    Text(ammo_str, style=ammo_style),
                )

        return Panel(table, title="Weapons", border_style="white")
