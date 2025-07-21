from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static
from textual.containers import Grid
from textual.binding import Binding
from ..widgets.weapon_list import WeaponListWidget

class InventoryScreen(ModalScreen):
    """The inventory screen."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("up", "move_selection(-1)", "Up"),
        Binding("down", "move_selection(1)", "Down"),
        Binding("left", "switch_focus", "Switch"),
        Binding("right", "switch_focus", "Switch"),
        Binding("enter", "select_item", "Select"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.focused_list = "inventory" # "inventory" or "attachments"
        self.selected_weapon_to_mount = None

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.update_inventory()
        self.update_focus()

    def update_inventory(self) -> None:
        """Update the inventory display."""
        gs = self.app.game_state
        
        # Car Preview
        car_preview = self.query_one("#car_preview", Static)
        car_art = "\n".join(gs.player_car.art.get("N", []))
        car_preview.update(car_art)
        
        # Attachments
        attachments_widget = self.query_one("#attachments", WeaponListWidget)
        attachments_widget.weapons = list(gs.mounted_weapons.values())
        
        # Inventory
        inventory_widget = self.query_one("#inventory", WeaponListWidget)
        inventory_widget.weapons = gs.player_inventory
        
        # Stats
        stats = self.query_one("#stats", Static)
        stats_str = f"""
        Durability: {gs.current_durability}/{gs.max_durability}
        Gas: {gs.current_gas:.0f}/{gs.gas_capacity}
        Speed: {gs.max_speed:.1f}
        Acceleration: {gs.acceleration_factor:.2f}
        Handling: {gs.turn_rate:.2f}
        """
        stats.update(stats_str)

    def update_focus(self) -> None:
        """Update the visual focus indicator."""
        inv_widget = self.query_one("#inventory", WeaponListWidget)
        att_widget = self.query_one("#attachments", WeaponListWidget)
        
        if self.focused_list == "inventory":
            inv_widget.border_title = "Inventory (Selected)"
            att_widget.border_title = "Attachments"
        else:
            inv_widget.border_title = "Inventory"
            att_widget.border_title = "Attachments (Selected)"

    def action_move_selection(self, amount: int) -> None:
        """Move the selection in the currently focused list."""
        if self.focused_list == "inventory":
            widget = self.query_one("#inventory", WeaponListWidget)
        else:
            widget = self.query_one("#attachments", WeaponListWidget)
        
        if widget.weapons:
            widget.selected_index = (widget.selected_index + amount + len(widget.weapons)) % len(widget.weapons)

    def action_switch_focus(self) -> None:
        """Switch focus between the inventory and attachment lists."""
        if self.selected_weapon_to_mount:
            # If we're in the middle of mounting, don't switch focus
            return
        self.focused_list = "attachments" if self.focused_list == "inventory" else "inventory"
        self.update_focus()

    def action_select_item(self) -> None:
        """Select an item to mount or a slot to mount it to."""
        gs = self.app.game_state
        
        if self.selected_weapon_to_mount:
            # We are selecting an attachment slot
            attachments_widget = self.query_one("#attachments", WeaponListWidget)
            slot_index = attachments_widget.selected_index
            slot_name = list(gs.mounted_weapons.keys())[slot_index]
            
            # Swap weapons
            currently_mounted = gs.mounted_weapons[slot_name]
            gs.mounted_weapons[slot_name] = self.selected_weapon_to_mount
            
            gs.player_inventory.remove(self.selected_weapon_to_mount)
            if currently_mounted:
                gs.player_inventory.append(currently_mounted)
            
            self.selected_weapon_to_mount = None
            self.focused_list = "inventory"
            self.update_inventory()
            self.update_focus()
            
        else:
            # We are selecting a weapon from the inventory
            if self.focused_list == "inventory":
                inventory_widget = self.query_one("#inventory", WeaponListWidget)
                if inventory_widget.weapons:
                    self.selected_weapon_to_mount = inventory_widget.weapons[inventory_widget.selected_index]
                    self.focused_list = "attachments"
                    self.update_focus()

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        with Grid(id="inventory_grid"):
            yield Static("Car Preview", id="car_preview")
            yield WeaponListWidget(id="attachments")
            yield WeaponListWidget(id="inventory")
            yield Static("Stats", id="stats")
        yield Footer()

