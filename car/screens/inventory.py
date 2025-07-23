from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static
from textual.containers import Grid, Vertical, ScrollableContainer
from textual.binding import Binding
from ..widgets.weapon_list import WeaponListWidget
from ..widgets.weapon_info import WeaponInfo
from ..logic.entity_loader import PLAYER_CARS

class InventoryScreen(ModalScreen):
    """The inventory screen."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("up", "move_selection(-1)", "Up"),
        Binding("down", "move_selection(1)", "Down"),
        Binding("left", "switch_focus", "Switch"),
        Binding("right", "switch_focus", "Switch"),
        Binding("a", "rotate_preview(-1)", "Rotate Left"),
        Binding("d", "rotate_preview(1)", "Rotate Right"),
        Binding("enter", "select_item", "Select"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.focused_list = "inventory" # "inventory" or "attachments"
        self.selected_weapon_to_mount = None
        self.selected_slot_to_fill = None
        self.unequip_confirmation_slot = None
        self.preview_angle = 0
        self.blink_timer = None
        self.blink_state = True

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.update_inventory()
        self.update_focus()
        self.blink_timer = self.set_interval(0.5, self.toggle_blink)

    def on_unmount(self) -> None:
        """Called when the screen is unmounted."""
        if self.blink_timer:
            self.blink_timer.stop()
        self.app.game_state.menu_open = False

    def toggle_blink(self) -> None:
        """Toggle the blink state for the attachment point marker."""
        self.blink_state = not self.blink_state
        self.update_inventory()

    def update_inventory(self) -> None:
        """Update the inventory display."""
        gs = self.app.game_state
        
        # Car Preview
        car_preview = self.query_one("#car_preview", Static)
        car_class = PLAYER_CARS[gs.selected_car_index]
        car_instance = car_class(0, 0)
        color = gs.car_color_names[0].lower().replace("car_", "")
        colored_art_dict = {}
        for direction, art_lines in car_instance.art.items():
            colored_art_dict[direction] = [f"[{color}]{line}[/]" for line in art_lines]
        car_instance.art = colored_art_dict
        art = self.get_art_for_angle(car_instance, self.preview_angle)
        art = self._overlay_attachment_points(art, car_instance)
        car_preview.update(art)
        
        # Attachments
        attachments_widget = self.query_one("#attachments", WeaponListWidget)
        attachments_widget.weapons = [
            {"name": f"{i+1}. {point_data['name']}: {weapon.name if weapon else '(' + point_data['level'] + ')'}"}
            for i, (point_data, weapon) in enumerate(zip(gs.attachment_points.values(), gs.mounted_weapons.values()))
        ]
        
        # Inventory
        inventory_widget = self.query_one("#inventory", WeaponListWidget)
        inventory_widget.weapons = gs.player_inventory
        
        # Stats
        stats = self.query_one("#stats", Static)
        ammo_str = "\n".join([f"- {ammo_type}: {count}" for ammo_type, count in gs.ammo_counts.items()])
        stats_str = f"""
        Quest: {gs.current_quest.name if gs.current_quest else 'None'}
        Level: {gs.player_level}
        XP: {gs.current_xp}/{gs.xp_to_next_level}

        Durability: {gs.current_durability}/{gs.max_durability}
        Gas: {gs.current_gas:.0f}/{gs.gas_capacity}
        
        Ammo:
        {ammo_str}
        """
        stats.update(stats_str)

    def get_art_for_angle(self, car_instance, angle):
        """Gets the correct vehicle art for a given angle."""
        angle = angle % 360
        if 337.5 <= angle or angle < 22.5: direction = "N"
        elif 22.5 <= angle < 67.5: direction = "NE"
        elif 67.5 <= angle < 112.5: direction = "E"
        elif 112.5 <= angle < 157.5: direction = "SE"
        elif 157.5 <= angle < 202.5: direction = "S"
        elif 202.5 <= angle < 247.5: direction = "SW"
        elif 247.5 <= angle < 292.5: direction = "W"
        else: direction = "NW"
        return "\n".join(car_instance.art.get(direction, [""]))

    def _overlay_attachment_points(self, art_str: str, car_instance) -> str:
        """Overlays attachment point indicators onto the car art."""
        art_lines = art_str.split("\n")
        art_height = len(art_lines)
        art_width = max(len(line.replace(f"[{'yellow'}]", "").replace("[/]", "")) for line in art_lines) if art_lines else 0
        
        # Create a mutable grid of characters
        grid = [list(line) for line in art_lines]

        attachments_widget = self.query_one("#attachments", WeaponListWidget)
        selected_slot_index = attachments_widget.selected_index

        for i, (point_name, point_data) in enumerate(car_instance.attachment_points.items()):
            # This is a simplified 2D projection
            # A real implementation would need to account for the car's rotation
            px = int(art_width / 2 + point_data["offset_x"])
            py = int(art_height / 2 + point_data["offset_y"])

            if 0 <= py < len(grid) and 0 <= px < len(grid[py]):
                marker = str(i + 1)
                if self.focused_list == "attachments" and i == selected_slot_index:
                    marker = "●" if self.blink_state else str(i + 1)
                
                grid[py][px] = f"[yellow]{marker}[/]"
        
        return "\n".join("".join(row) for row in grid)

    def update_focus(self) -> None:
        """Update the visual focus indicator."""
        inv_widget = self.query_one("#inventory", WeaponListWidget)
        att_widget = self.query_one("#attachments", WeaponListWidget)
        
        if self.focused_list == "inventory":
            inv_widget.border_title = "Inventory (Selected)"
            att_widget.border_title = "Loadout"
        else:
            inv_widget.border_title = "Inventory"
            att_widget.border_title = "Loadout (Selected)"

    def action_move_selection(self, amount: int) -> None:
        """Move the selection in the currently focused list."""
        self.unequip_confirmation_slot = None # Cancel unequip on move
        if self.focused_list == "inventory":
            widget = self.query_one("#inventory", WeaponListWidget)
        else:
            widget = self.query_one("#attachments", WeaponListWidget)
        
        if widget.weapons:
            widget.selected_index = (widget.selected_index + amount + len(widget.weapons)) % len(widget.weapons)
            self.update_weapon_info()

    def update_weapon_info(self) -> None:
        """Update the weapon info panel based on the current selection."""
        weapon_to_display = None
        
        if self.focused_list == "inventory":
            widget = self.query_one("#inventory", WeaponListWidget)
            if widget.weapons:
                weapon_to_display = widget.weapons[widget.selected_index]
        else: # attachments
            widget = self.query_one("#attachments", WeaponListWidget)
            if widget.weapons:
                slot_name = list(self.app.game_state.mounted_weapons.keys())[widget.selected_index]
                weapon_to_display = self.app.game_state.mounted_weapons[slot_name]

        weapon_info = self.query_one("#weapon_info", WeaponInfo)
        if weapon_to_display:
            weapon_info.name = weapon_to_display.name
            weapon_info.damage = weapon_to_display.damage
            weapon_info.range = weapon_to_display.range
            weapon_info.fire_rate = weapon_to_display.fire_rate
            
            modifier_str = "\n".join([f"- {mod}: {val}" for mod, val in weapon_to_display.modifiers.items()])
            weapon_info.modifiers = f"Modifiers:\n{modifier_str}"
        else:
            weapon_info.name = "N/A"
            weapon_info.damage = 0
            weapon_info.range = 0
            weapon_info.fire_rate = 0
            weapon_info.modifiers = ""

    def action_rotate_preview(self, direction: int) -> None:
        """Rotate the car preview."""
        self.preview_angle += 45 * direction
        self.update_inventory()

    def action_switch_focus(self) -> None:
        """Switch focus between the inventory and attachment lists."""
        self.unequip_confirmation_slot = None # Cancel unequip on switch
        if self.selected_weapon_to_mount or self.selected_slot_to_fill:
            return
        self.focused_list = "attachments" if self.focused_list == "inventory" else "inventory"
        self.update_focus()

    def action_select_item(self) -> None:
        """Select an item to mount or a slot to mount it to."""
        gs = self.app.game_state
        
        if self.focused_list == "inventory":
            # --- INVENTORY focused ---
            inv_widget = self.query_one("#inventory", WeaponListWidget)
            if not inv_widget.weapons: return

            selected_weapon = inv_widget.weapons[inv_widget.selected_index]

            if self.selected_slot_to_fill:
                # Equip selected weapon to staged slot
                slot_name = self.selected_slot_to_fill
                currently_mounted = gs.mounted_weapons[slot_name]
                gs.mounted_weapons[slot_name] = selected_weapon
                gs.player_inventory.remove(selected_weapon)
                if currently_mounted:
                    gs.player_inventory.append(currently_mounted)
                
                self.selected_slot_to_fill = None
                self.focused_list = "attachments"
            else:
                # Stage selected weapon for equipping
                self.selected_weapon_to_mount = selected_weapon
                self.focused_list = "attachments"

        else:
            # --- ATTACHMENTS focused ---
            att_widget = self.query_one("#attachments", WeaponListWidget)
            slot_index = att_widget.selected_index
            slot_name = list(gs.mounted_weapons.keys())[slot_index]
            
            if self.selected_weapon_to_mount:
                # Equip staged weapon to selected slot
                currently_mounted = gs.mounted_weapons[slot_name]
                gs.mounted_weapons[slot_name] = self.selected_weapon_to_mount
                gs.player_inventory.remove(self.selected_weapon_to_mount)
                if currently_mounted:
                    gs.player_inventory.append(currently_mounted)
                
                self.selected_weapon_to_mount = None
                self.focused_list = "inventory"
            else:
                # No weapon staged, so either unequip or stage the slot
                if gs.mounted_weapons[slot_name]:
                    # Slot is equipped, check for unequip confirmation
                    if self.unequip_confirmation_slot == slot_name:
                        # Unequip the weapon
                        weapon_to_unequip = gs.mounted_weapons[slot_name]
                        gs.mounted_weapons[slot_name] = None
                        gs.player_inventory.append(weapon_to_unequip)
                        self.unequip_confirmation_slot = None
                    else:
                        # First press, stage for unequip
                        self.unequip_confirmation_slot = slot_name
                else:
                    # Slot is empty, stage it for filling
                    self.selected_slot_to_fill = slot_name
                    self.focused_list = "inventory"

        self.update_inventory()
        self.update_focus()

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        with Grid(id="inventory_grid"):
            with Vertical():
                yield Static("Car Preview", id="car_preview")
                yield WeaponListWidget(id="attachments")
            with Vertical():
                with ScrollableContainer():
                    yield WeaponListWidget(id="inventory")
                yield WeaponInfo(id="weapon_info")
                yield Static("Stats", id="stats")
        yield Footer()