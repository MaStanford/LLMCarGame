from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Grid
from textual.binding import Binding
from ..widgets.weapon_info import WeaponInfo
from ..logic.shop_logic import get_shop_inventory, purchase_item

class ShopScreen(ModalScreen):
    """The shop screen."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("up", "move_selection(-1)", "Up"),
        Binding("down", "move_selection(1)", "Down"),
    ]

    def __init__(self, shop_type: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.shop_type = shop_type
        self.inventory = []
        self.selected_index = 0

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.inventory = get_shop_inventory(self.shop_type, self.app.game_state)
        self.update_shop_display()

    def update_shop_display(self) -> None:
        """Update the shop's display."""
        # Item List
        item_list = self.query_one("#item_list", Static)
        list_str = ""
        for i, item in enumerate(self.inventory):
            price = item.get('price', 'N/A')
            name = item.get('name', 'Unknown Item')
            if i == self.selected_index:
                list_str += f"> {name} (${price})\n"
            else:
                list_str += f"  {name} (${price})\n"
        item_list.update(list_str)

        # Item Info
        if self.inventory:
            selected_item = self.inventory[self.selected_index]
            if selected_item.get("type") == "weapon":
                weapon_info = self.query_one("#item_info", WeaponInfo)
                weapon_info.name = selected_item["name"]
                weapon_info.damage = selected_item["damage"]
                weapon_info.range = selected_item["range"]
                weapon_info.fire_rate = selected_item["fire_rate"]
    
    def action_move_selection(self, amount: int) -> None:
        """Move the selection in the item list."""
        self.selected_index = (self.selected_index + amount + len(self.inventory)) % len(self.inventory)
        self.update_shop_display()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle buy button presses."""
        if event.button.id == "buy_item":
            if self.inventory:
                selected_item = self.inventory[self.selected_index]
                price = selected_item.get("price", 0)
                if self.app.game_state.player_cash >= price:
                    self.app.game_state.player_cash -= price
                    purchase_item(self.app.game_state, selected_item)
                    self.app.screen.query_one("#notifications").add_notification(f"Purchased {selected_item['name']}!")
                    # Refresh the inventory in case it's dynamic
                    self.inventory = get_shop_inventory(self.shop_type, self.app.game_state)
                    self.update_shop_display()
                else:
                    self.app.screen.query_one("#notifications").add_notification("Not enough cash!")

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        with Grid(id="shop_grid"):
            yield Static("For Sale", id="item_list")
            yield WeaponInfo(id="item_info")
            yield Button("Buy", id="buy_item", variant="primary")
        yield Footer()
