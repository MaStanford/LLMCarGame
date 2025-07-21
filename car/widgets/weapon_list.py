from textual.widgets import Static
from textual.reactive import reactive

class WeaponListWidget(Static):
    """A widget to display a list of weapons."""

    weapons = reactive([])
    selected_index = reactive(0)

    def on_mount(self) -> None:
        """Called when the widget is mounted."""
        self.update_render()

    def watch_weapons(self, new_weapons) -> None:
        """Called when the weapons list changes."""
        self.selected_index = 0
        self.update_render()

    def watch_selected_index(self, new_index) -> None:
        """Called when the selected index changes."""
        self.update_render()

    def update_render(self) -> None:
        """Update the displayed list."""
        list_str = ""
        for i, weapon in enumerate(self.weapons):
            if i == self.selected_index:
                list_str += f"> {weapon.name}\n"
            else:
                list_str += f"  {weapon.name}\n"
        self.update(list_str)

