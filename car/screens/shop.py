import math
from functools import partial
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Grid, Vertical
from textual.binding import Binding
from textual.worker import Worker, WorkerState

from ..widgets.item_list import ItemListWidget
from ..widgets.item_info import ItemInfoWidget
from ..widgets.menu_stats_hud import MenuStatsHUD
from ..logic.shop_logic import get_shop_inventory, purchase_item, calculate_sell_price
from ..world.generation import get_city_faction
from ..data.game_constants import CITY_SPACING
from ..workers.dialog_generator import generate_dialog_worker

class ShopScreen(Screen):
    """The shop screen."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("up", "move_selection(-1)", "Up"),
        Binding("down", "move_selection(1)", "Down"),
        Binding("left", "switch_focus", "Switch"),
        Binding("right", "switch_focus", "Switch"),
        Binding("enter", "select_item", "Select"),
    ]

    def __init__(self, shop_type: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.shop_type = shop_type
        self.shop_inventory = []
        self.focused_list = "shop"  # "shop" or "player"
        self.sell_confirmation_item = None

    def _notify(self, message: str):
        """Post a notification to the WorldScreen."""
        try:
            self.app.screen_stack[-2].query_one("#notifications").add_notification(message)
        except Exception:
            pass # Fail silently

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.update_displays()
        self.update_focus()
        self.generate_dialog()

    def generate_dialog(self):
        """Starts a worker to generate shopkeeper dialog."""
        gs = self.app.game_state
        faction_data = self.app.data.factions.FACTION_DATA
        
        city_faction_id = get_city_faction(gs.car_world_x, gs.car_world_y)
        faction_info = faction_data.get(city_faction_id, {})
        faction_name = faction_info.get("name", "The Wasteland")
        faction_vibe = faction_info.get("description", "A desolate, lawless place.")
        player_rep = gs.faction_reputation.get(city_faction_id, 0)

        worker_callable = partial(
            generate_dialog_worker,
            app=self.app,
            theme=gs.theme,
            shop_type=self.shop_type,
            faction_name=faction_name,
            faction_vibe=faction_vibe,
            player_reputation=player_rep
        )
        self.run_worker(worker_callable, exclusive=True, name="DialogGenerator")

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Handle completed dialog worker."""
        if event.worker.name == "DialogGenerator" and event.worker.state == WorkerState.SUCCESS:
            dialog = event.worker.result
            self.query_one("#shop_dialog", Static).update(dialog)

    def on_unmount(self) -> None:
        """Called when the screen is unmounted."""
        gs = self.app.game_state
        gs.menu_open = False
        # ... (rest of the unmount logic is the same)

    def update_displays(self) -> None:
        """Update all display widgets."""
        gs = self.app.game_state
        
        # Shop Inventory
        self.shop_inventory = get_shop_inventory(self.shop_type, gs)
        shop_widget = self.query_one("#shop_inventory", ItemListWidget)
        shop_widget.items = self.shop_inventory
        
        # Player Inventory
        player_widget = self.query_one("#player_inventory", ItemListWidget)
        player_widget.items = gs.player_inventory
        
        # Stats
        self.query_one(MenuStatsHUD).update_stats(gs)
        
        self.update_item_info()
        self.update_action_button()

    def update_focus(self) -> None:
        """Update the visual focus indicator."""
        shop_widget = self.query_one("#shop_inventory", ItemListWidget)
        player_widget = self.query_one("#player_inventory", ItemListWidget)
        
        if self.focused_list == "shop":
            shop_widget.border_title = "Shop (Selected)"
            player_widget.border_title = "Your Inventory"
        else:
            shop_widget.border_title = "Shop"
            player_widget.border_title = "Your Inventory (Selected)"

    def update_action_button(self) -> None:
        """Update the main action button's label and state."""
        button = self.query_one("#action_button", Button)
        can_sell = self.shop_type == "weapon_shop"

        if self.focused_list == "shop":
            button.label = "Buy"
            button.disabled = not self.shop_inventory
        elif can_sell:
            player_widget = self.query_one("#player_inventory", ItemListWidget)
            selected_item = player_widget.selected_item
            if self.sell_confirmation_item == selected_item and selected_item is not None:
                price = calculate_sell_price(selected_item, self.app.game_state)
                button.label = f"Confirm Sell (${price})?"
            else:
                button.label = "Sell"
            button.disabled = not player_widget.items
        else: # Player focus, but can't sell
            button.label = "Sell"
            button.disabled = True

    def action_move_selection(self, amount: int) -> None:
        """Move the selection in the currently focused list."""
        self.sell_confirmation_item = None # Reset confirmation on move
        if self.focused_list == "shop":
            widget = self.query_one("#shop_inventory", ItemListWidget)
        else:
            widget = self.query_one("#player_inventory", ItemListWidget)
        
        if widget.items:
            widget.selected_index = (widget.selected_index + amount + len(widget.items)) % len(widget.items)
            self.update_item_info()
            self.update_action_button()

    def update_item_info(self) -> None:
        """Update the item info panel based on the current selection."""
        if self.focused_list == "shop":
            widget = self.query_one("#shop_inventory", ItemListWidget)
            item_to_display = widget.selected_item
        else:
            widget = self.query_one("#player_inventory", ItemListWidget)
            item_to_display = widget.selected_item

        self.query_one(ItemInfoWidget).display_item(item_to_display)

    def action_switch_focus(self) -> None:
        """Switch focus between the shop and player inventory lists."""
        self.sell_confirmation_item = None # Reset confirmation on switch
        self.focused_list = "player" if self.focused_list == "shop" else "shop"
        self.update_focus()
        self.update_item_info()
        self.update_action_button()

    def action_select_item(self) -> None:
        """Handle buying or selling the selected item."""
        if self.focused_list == "shop":
            self._buy_item()
        else:
            self._sell_item()
        self.update_action_button()

    def _buy_item(self):
        """Logic for purchasing an item."""
        gs = self.app.game_state
        shop_widget = self.query_one("#shop_inventory", ItemListWidget)
        selected_item = shop_widget.selected_item
        if not selected_item: return

        price = selected_item.get("price", 0)
        if gs.player_cash >= price:
            gs.player_cash -= price
            purchase_item(gs, selected_item)
            self._notify(f"Purchased {selected_item['name']}!")
            self.update_displays()
        else:
            self._notify("Not enough cash!")

    def _sell_item(self):
        """Logic for selling an item."""
        if self.shop_type != "weapon_shop":
            self._notify("You cannot sell items at this shop.")
            return

        gs = self.app.game_state
        player_widget = self.query_one("#player_inventory", ItemListWidget)
        selected_item = player_widget.selected_item
        if not selected_item: return

        if self.sell_confirmation_item == selected_item:
            # Second press: confirm sell
            price = calculate_sell_price(selected_item, gs)
            gs.player_cash += price
            gs.player_inventory.remove(selected_item)
            self._notify(f"Sold {selected_item.name} for ${price}!")
            self.sell_confirmation_item = None
            self.update_displays()
        else:
            # First press: stage for confirmation
            self.sell_confirmation_item = selected_item

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        with Grid(id="shop_grid"):
            # Top-Left: Shop Inventory
            yield ItemListWidget(id="shop_inventory")
            
            # Top-Right: Player Inventory
            yield ItemListWidget(id="player_inventory")

            # Bottom-Left: Shopkeeper Dialog
            yield Static("Welcome, traveler!", id="shop_dialog")

            # Bottom-Right: Player Info & Actions
            with Vertical():
                yield ItemInfoWidget()
                yield MenuStatsHUD()
                yield Button("Buy/Sell", id="action_button", variant="primary")
        yield Footer()