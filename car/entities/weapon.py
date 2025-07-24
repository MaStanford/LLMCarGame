import uuid
from ..data.weapons import WEAPONS_DATA

class Weapon:
    def __init__(self, weapon_type_id, modifiers=None, instance_id=None):
        self.weapon_type_id = weapon_type_id
        self.base_stats = WEAPONS_DATA[self.weapon_type_id]
        self.modifiers = modifiers if modifiers else {}
        self.instance_id = instance_id if instance_id else str(uuid.uuid4())

    @property
    def type(self):
        return "weapon"

    @property
    def name(self):
        return self.base_stats["name"]

    @property
    def damage(self):
        base_damage = self.base_stats["power"]
        if "damage_boost" in self.modifiers:
            base_damage *= self.modifiers["damage_boost"]
        return base_damage

    @property
    def fire_rate(self):
        base_fire_rate = self.base_stats["fire_rate"]
        if "fire_rate_boost" in self.modifiers:
            base_fire_rate *= self.modifiers["fire_rate_boost"]
        return base_fire_rate

    @property
    def range(self):
        base_range = self.base_stats["range"]
        if "range_boost" in self.modifiers:
            base_range *= self.modifiers["range_boost"]
        return base_range

    @property
    def pellet_count(self):
        base_pellet_count = self.base_stats.get("pellet_count", 1)
        if "pellet_count_boost" in self.modifiers:
            base_pellet_count += self.modifiers["pellet_count_boost"]
        return base_pellet_count

    @property
    def spread_angle(self):
        return self.base_stats.get("spread_angle", 0)
        
    @property
    def ammo_type(self):
        return self.base_stats["ammo_type"]
        
    @property
    def particle(self):
        return self.base_stats["particle"]
        
    @property
    def art(self):
        return self.base_stats["art"]

    @property
    def speed(self):
        return self.base_stats["speed"]

    @property
    def slots(self):
        return self.base_stats["slots"]

    def to_dict(self):
        """Serializes the weapon to a dictionary."""
        return {
            "weapon_type_id": self.weapon_type_id,
            "modifiers": self.modifiers,
            "instance_id": self.instance_id,
        }

    @classmethod
    def from_dict(cls, data):
        """Deserializes a dictionary back into a Weapon object."""
        return cls(
            weapon_type_id=data["weapon_type_id"],
            modifiers=data.get("modifiers"),
            instance_id=data.get("instance_id"),
        )
