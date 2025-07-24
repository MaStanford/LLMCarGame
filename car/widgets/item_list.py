from textual.widgets import Static
from textual.reactive import reactive
from rich.table import Table
from rich.text import Text

class ItemListWidget(Static):
    """A widget to display a list of items with prices."""

    items = reactive([])
    selected_index = reactive(0)

    @property
    def selected_item(self):
        """Returns the currently selected item data, or None."""
        if self.items and 0 <= self.selected_index < len(self.items):
            return self.items[self.selected_index]
        return None

    def on_mount(self) -> None:
        """Called when the widget is mounted."""
        self.update_render()

    def watch_items(self, new_items) -> None:
        """Called when the items list changes."""
        self.selected_index = 0
        self.update_render()

    def watch_selected_index(self, new_index) -> None:
        """Called when the selected index changes."""
        self.update_render()

    def update_render(self) -> None:
        """Update the displayed list."""
        table = Table(show_header=False, expand=True, box=None, padding=0)
        table.add_column("Name", justify="left", no_wrap=True)
        table.add_column("Price", justify="right", no_wrap=True)

        for i, item_data in enumerate(self.items):
            name = ""
            price_str = ""
            
            # Handle both dicts from shops and Weapon objects from inventory
            if isinstance(item_data, dict):
                name = item_data.get("name", "Unknown")
                price = item_data.get("price")
                if price is not None:
                    price_str = f"${price}"
            elif hasattr(item_data, "name"):
                name = item_data.name
                if hasattr(item_data, "price"):
                     price_str = f"${item_data.price}"


            row_style = "reverse" if i == self.selected_index else ""
            table.add_row(
                Text(name, style=row_style),
                Text(price_str, style=row_style)
            )
        self.update(table)