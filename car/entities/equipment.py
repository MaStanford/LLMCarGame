import uuid
from ..data.equipment import EQUIPMENT_DATA

class Equipment:
    def __init__(self, equipment_type_id, modifiers=None, instance_id=None, name=None, description=None, rarity=None):
        self.equipment_type_id = equipment_type_id
        self.base_stats = EQUIPMENT_DATA[self.equipment_type_id]
        self.modifiers = modifiers if modifiers else {}
        self.instance_id = instance_id if instance_id else str(uuid.uuid4())
        self.custom_name = name
        self.custom_description = description
        self.rarity = rarity if rarity else "common"

    @property
    def type(self):
        return "equipment"

    @property
    def name(self):
        return self.custom_name or self.base_stats["name"]

    @property
    def description(self):
        return self.custom_description or self.base_stats.get("description", "Standard equipment.")

    @property
    def price(self):
        return self.base_stats["price"]

    @property
    def slot(self):
        return self.base_stats["slot"]

    @property
    def stat_bonuses(self):
        """Returns the final stat bonuses dict after applying rarity modifiers."""
        bonuses = dict(self.base_stats.get("bonuses", {}))
        for stat, value in bonuses.items():
            modifier_key = f"{stat}_boost"
            if modifier_key in self.modifiers:
                bonuses[stat] = round(value * self.modifiers[modifier_key], 3)
        return bonuses

    @property
    def scrap_value(self):
        base_scrap = self.base_stats.get("scrap_value", 5)
        rarity_multipliers = {"common": 1, "uncommon": 2, "rare": 4, "epic": 8, "legendary": 16}
        return base_scrap * rarity_multipliers.get(self.rarity, 1)

    def __eq__(self, other):
        if not isinstance(other, Equipment):
            return False
        return self.instance_id == other.instance_id

    def __hash__(self):
        return hash(self.instance_id)

    def to_dict(self):
        return {
            "item_type": "equipment",
            "equipment_type_id": self.equipment_type_id,
            "modifiers": self.modifiers,
            "instance_id": self.instance_id,
            "custom_name": self.custom_name,
            "custom_description": self.custom_description,
            "rarity": self.rarity,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            equipment_type_id=data["equipment_type_id"],
            modifiers=data.get("modifiers"),
            instance_id=data.get("instance_id"),
            name=data.get("custom_name"),
            description=data.get("custom_description"),
            rarity=data.get("rarity"),
        )
