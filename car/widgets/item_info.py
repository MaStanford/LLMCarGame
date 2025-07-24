from textual.widgets import Static
from rich.panel import Panel
from rich.text import Text

class ItemInfoWidget(Static):
    """A widget to display contextual information about an item."""

    def display_item(self, item_data) -> None:
        """Update the display with info about the given item."""
        if not item_data:
            self.update(Panel("Select an item", title="Info"))
            return

        # Handle both dicts from shops and Weapon objects from inventory
        if isinstance(item_data, dict):
            item_type = item_data.get('type')
            name = item_data.get('name', "N/A")
            damage = item_data.get('damage', 0)
            range_ = item_data.get('range', 0)
            fire_rate = item_data.get('fire_rate', 0)
            ammo_type = item_data.get('ammo_type', 'N/A')
            mods = item_data.get('modifiers', {})
        else: # It's an object
            item_type = getattr(item_data, 'type', None)
            name = getattr(item_data, 'name', "N/A")
            damage = getattr(item_data, 'damage', 0)
            range_ = getattr(item_data, 'range', 0)
            fire_rate = getattr(item_data, 'fire_rate', 0)
            ammo_type = getattr(item_data, 'ammo_type', 'N/A')
            mods = getattr(item_data, 'modifiers', {})

        content = ""
        if item_type == "weapon":
            content = (
                f"Damage: {damage}\n"
                f"Range: {range_}\n"
                f"Fire Rate: {fire_rate}\n"
                f"Ammo Type: {ammo_type}\n"
            )
            if mods:
                modifier_str = "\n".join([f"- {mod}: {val}" for mod, val in mods.items()])
                content += f"Modifiers:\n{modifier_str}"

        elif item_type == "repair":
            content = "Repairs the vehicle to its maximum durability."
        
        elif item_type == "gas":
            content = "Fills the vehicle's gas tank to capacity."
            
        else:
            content = "A standard item."

        self.update(Panel(Text(content), title=name))
