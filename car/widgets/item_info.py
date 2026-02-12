from textual.widgets import Static
from rich.panel import Panel
from rich.text import Text
from ..data.modifiers import RARITY_TIERS

RARITY_COLORS = {r: d["color"] for r, d in RARITY_TIERS.items()}

class ItemInfoWidget(Static):
    """A widget to display contextual information about an item."""

    def display_item(self, item_data) -> None:
        """Update the display with info about the given item."""
        if not item_data:
            self.update(Panel("Select an item", title="Info"))
            return

        # Handle both dicts from shops and Weapon/Equipment objects from inventory
        if isinstance(item_data, dict):
            item_type = item_data.get('type')
            name = item_data.get('name', "N/A")
            rarity = item_data.get('rarity', 'common')
            mods = item_data.get('modifiers', {})
        else: # It's an object
            item_type = getattr(item_data, 'type', None)
            name = getattr(item_data, 'name', "N/A")
            rarity = getattr(item_data, 'rarity', 'common')
            mods = getattr(item_data, 'modifiers', {})

        content = ""
        rarity_color = RARITY_COLORS.get(rarity, "white")

        if item_type == "weapon":
            if isinstance(item_data, dict):
                damage = item_data.get('damage', 0)
                range_ = item_data.get('range', 0)
                fire_rate = item_data.get('fire_rate', 0)
                ammo_type = item_data.get('ammo_type', 'N/A')
            else:
                damage = getattr(item_data, 'damage', 0)
                range_ = getattr(item_data, 'range', 0)
                fire_rate = getattr(item_data, 'fire_rate', 0)
                ammo_type = getattr(item_data, 'ammo_type', 'N/A')

            content = f"[{rarity_color}]{rarity.upper()}[/]\n"
            content += (
                f"Damage: {damage}\n"
                f"Range: {range_}\n"
                f"Fire Rate: {fire_rate}\n"
                f"Ammo Type: {ammo_type}\n"
            )
            if mods:
                modifier_str = "\n".join([f"- {mod}: {val}" for mod, val in mods.items()])
                content += f"Modifiers:\n{modifier_str}"

        elif item_type == "equipment":
            if isinstance(item_data, dict):
                slot = item_data.get("slot", "N/A")
                desc = item_data.get("description", "")
                bonuses = item_data.get("bonuses", {})
            else:
                slot = getattr(item_data, "slot", "N/A")
                desc = getattr(item_data, "description", "")
                bonuses = getattr(item_data, "stat_bonuses", {})

            content = f"[{rarity_color}]{rarity.upper()}[/]\n"
            content += f"Slot: {slot.title()}\n"
            content += f"{desc}\n\n"
            content += "Stat Bonuses:\n"
            for stat, val in bonuses.items():
                percent = int((val - 1.0) * 100)
                sign = "+" if percent >= 0 else ""
                content += f"  {stat.replace('_', ' ').title()}: {sign}{percent}%\n"
            if mods:
                modifier_str = "\n".join([f"  {mod}: {val}" for mod, val in mods.items()])
                content += f"\nModifiers:\n{modifier_str}"

        elif item_type == "repair":
            content = "Repairs the vehicle to its maximum durability."

        elif item_type == "gas":
            content = "Fills the vehicle's gas tank to capacity."

        elif item_type == "ammo":
            ammo_type = item_data.get("ammo_type", "N/A") if isinstance(item_data, dict) else "N/A"
            amount = item_data.get("amount", 0) if isinstance(item_data, dict) else 0
            content = f"Ammo Type: {ammo_type}\nQuantity: {amount}"

        else:
            content = "A standard item."

        self.update(Panel(Text.from_markup(content), title=name))
