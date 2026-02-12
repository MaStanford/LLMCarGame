# --- Equipment Slot Definitions ---
EQUIPMENT_SLOTS = {
    "armor":     {"name": "Armor Plating", "description": "Protective hull plating."},
    "engine":    {"name": "Engine Mod",    "description": "Engine performance upgrade."},
    "tires":     {"name": "Tires",         "description": "Tire modifications for handling."},
    "accessory": {"name": "Accessory",     "description": "Utility gadget or device."},
}

# --- Equipment Definitions ---
EQUIPMENT_DATA = {
    # --- Armor (mechanic shop) ---
    "eq_scrap_plating": {
        "id": "eq_scrap_plating",
        "name": "Scrap Plating",
        "slot": "armor",
        "description": "Welded scrap metal sheets. Better than nothing.",
        "bonuses": {"durability": 1.10},
        "price": 200,
        "scrap_value": 3,
        "shop_affinity": "mechanic",
    },
    "eq_reinforced_hull": {
        "id": "eq_reinforced_hull",
        "name": "Reinforced Hull",
        "slot": "armor",
        "description": "Pre-war military-grade plating.",
        "bonuses": {"durability": 1.25, "speed": 0.95},
        "price": 800,
        "scrap_value": 8,
        "shop_affinity": "mechanic",
    },
    "eq_reactive_armor": {
        "id": "eq_reactive_armor",
        "name": "Reactive Armor",
        "slot": "armor",
        "description": "Explosive-reactive plating that absorbs impact.",
        "bonuses": {"durability": 1.40, "speed": 0.90},
        "price": 2000,
        "scrap_value": 15,
        "shop_affinity": "mechanic",
    },

    # --- Tires (mechanic shop) ---
    "eq_offroad_tires": {
        "id": "eq_offroad_tires",
        "name": "Off-Road Tires",
        "slot": "tires",
        "description": "Knobby tires for rough terrain.",
        "bonuses": {"handling": 1.15, "braking": 1.10},
        "price": 300,
        "scrap_value": 3,
        "shop_affinity": "mechanic",
    },
    "eq_racing_slicks": {
        "id": "eq_racing_slicks",
        "name": "Racing Slicks",
        "slot": "tires",
        "description": "Smooth tires for maximum speed on roads.",
        "bonuses": {"speed": 1.10, "handling": 1.20, "braking": 1.15},
        "price": 700,
        "scrap_value": 5,
        "shop_affinity": "mechanic",
    },
    "eq_spiked_tires": {
        "id": "eq_spiked_tires",
        "name": "Spiked Tires",
        "slot": "tires",
        "description": "Metal-spiked tires. Good grip, loud.",
        "bonuses": {"handling": 1.10, "collision_damage": 1.20},
        "price": 400,
        "scrap_value": 4,
        "shop_affinity": "mechanic",
    },

    # --- Accessories (mechanic shop) ---
    "eq_ram_bar": {
        "id": "eq_ram_bar",
        "name": "Ram Bar",
        "slot": "accessory",
        "description": "Heavy front-mounted ram bar for smashing.",
        "bonuses": {"collision_damage": 1.30, "durability": 1.05},
        "price": 350,
        "scrap_value": 4,
        "shop_affinity": "mechanic",
    },

    # --- Engine (weapon shop) ---
    "eq_turbo_charger": {
        "id": "eq_turbo_charger",
        "name": "Turbo Charger",
        "slot": "engine",
        "description": "Bolted-on turbo. More speed, more fuel.",
        "bonuses": {"speed": 1.15, "acceleration": 1.10, "fuel_efficiency": 0.90},
        "price": 500,
        "scrap_value": 5,
        "shop_affinity": "weapon",
    },
    "eq_supercharger": {
        "id": "eq_supercharger",
        "name": "Supercharger",
        "slot": "engine",
        "description": "Belt-driven power. Serious speed.",
        "bonuses": {"speed": 1.25, "acceleration": 1.20, "fuel_efficiency": 0.85},
        "price": 1500,
        "scrap_value": 12,
        "shop_affinity": "weapon",
    },

    # --- Accessories (weapon shop) ---
    "eq_scope": {
        "id": "eq_scope",
        "name": "Targeting Scope",
        "slot": "accessory",
        "description": "Improved weapon aiming system.",
        "bonuses": {"weapon_aim_speed": 1.25, "damage": 1.05},
        "price": 400,
        "scrap_value": 4,
        "shop_affinity": "weapon",
    },
    "eq_fuel_tank": {
        "id": "eq_fuel_tank",
        "name": "Extra Fuel Tank",
        "slot": "accessory",
        "description": "Bolted-on auxiliary fuel tank.",
        "bonuses": {"fuel_capacity": 1.25},
        "price": 250,
        "scrap_value": 3,
        "shop_affinity": "weapon",
    },
    "eq_ammo_feeder": {
        "id": "eq_ammo_feeder",
        "name": "Ammo Feeder",
        "slot": "accessory",
        "description": "Auto-feed mechanism. Faster fire rate across all weapons.",
        "bonuses": {"fire_rate": 1.15},
        "price": 500,
        "scrap_value": 5,
        "shop_affinity": "weapon",
    },
}
