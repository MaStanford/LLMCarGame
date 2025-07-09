# --- Car Definitions & Stats ---
# Replaced emojis in car art
CARS_DATA = [
    { # 0: Hatchback
        "name": "Hatchback",
        "hp": 100, "weight": 10, "drag": 0.04, "braking": 12, "turn_rate": 0.12,
        "durability": 80, "gas_capacity": 5000, "gas_consumption": 0.08,
        "attachment_points": {
            "hood_center": {"offset_x": 2, "offset_y": 0, "size": 1},
            "roof": {"offset_x": 0, "offset_y": -1, "size": 2},
            "bumper": {"offset_x": 3, "offset_y": 0, "size": 1}
        },
        "mounted_weapons": {"hood_center": "lmg"},
        "ammo_bullet": 200, "ammo_heavy_bullet": 0, "ammo_fuel": 0,
        "inventory": [], # Initial inventory
        "menu_art": [
            r"    ╭──╮    ",
            r"  ╱ ◎ ◎╲  ",
            r" ╒══════╕ ",
            r" │ ═══> │ ",
            r" ╘══════╛ ",
            r"  ╰─☉☉─╯  ",
        ],
        "art": [
            [ r"  ┌──┐  ", r" ╱ ◎◎\\", r"│(═══>│", r" ╲ ☉☉╱ ", r"  └──┘ " ], # R
            [ r" ┌──╮ ", r" │◎╲╲", r" │ ◎=│", r" ╰─☉╱ ", r"   ╰┘ " ], # DR
            [ r"┌────┐", r"│◎──◎│", r"│ V══│", r"│╲☉☉╱│", r"└────┘" ], # D
            [ r" ╭──┐ ", r"╱╱◎ │", r"│=◎ │", r"╲☉─╯ ", r" └╯   " ], # DL
            [ r"  ┌──┐  ", r" ╱╱◎◎ ╲", r"│<═══)│", r" ╲ ☉☉╱ ", r"  └──┘  " ], # L
            [ r" ╭──┘ ", r"╱╱^ │", r"│=◎ │", r"╲☉─╮ ", r" `┘   " ], # UL
            [ r"┌────┐", r"│◎──◎│", r"│ ^══│", r"│╱☉☉╲│", r"└────┘" ], # U
            [ r"  ┌──╮", r" ╱^ ◎│", r"│= ◎ │", r" ☉─╯╱ ", r"┘    " ]  # UR
        ]
    },
    { # 1: Sports Car
        "name": "Sports Car",
        "hp": 180, "weight": 8, "drag": 0.03, "braking": 15, "turn_rate": 0.20,
        "durability": 60, "gas_capacity": 4000, "gas_consumption": 0.12,
        "attachment_points": {
            "hood_center": {"offset_x": 3, "offset_y": 0, "size": 1},
            "roof": {"offset_x": 0, "offset_y": -1, "size": 2},
            "bumper": {"offset_x": 4, "offset_y": 0, "size": 1}
        },
        "mounted_weapons": {"hood_center": "lmg"},
        "ammo_bullet": 150, "ammo_heavy_bullet": 0, "ammo_fuel": 0,
        "inventory": [], # Initial inventory
        "menu_art": [
            r"    ______    ",
            r" __╱ ◎  ◎ ╲__ ",
            r"╱__(═ > ═)__╲", # Simple arrow
            r"╲___☉──☉___╱",
        ],
        "art": [
            [ r"   ____╱ ", r" _╱ ◎ ◎\\", r"╱__(═>═)╲", r"╲___☉─☉╱ " ], # R
            [ r"  __ ╱", r" ╱ ◎╲╲", r"│◎═╦═│", r"╲_☉─╱ ", r"  `┘ " ], # DR
            [ r" ╱──────╲ ", r"│  ◎  ◎  │", r"│ V════V │", r" ╲☉────☉╱ " ], # D
            [ r" ╲ __  ", r" ╱╱◎ ╲ ", r"│═╦═◎│", r" ╲─☉_╱ ", r"  └┘  " ], # DL
            [ r" ╲____   ", r"╱╱ ◎ ◎╲_", r"╱(═<═)__╲", r" ╲☉──☉___╱" ], # L
            [ r" ╲ _   ", r"╱╱^◎╲ ", r"│═╦═◎│", r" ╲─☉_╲ ", r"   └┘ " ], # UL
            [ r" ╱──────╲ ", r"│╱╲____╱╲│", r"│ ^════^ │", r"│  ◎  ◎  │" ], # U
            [ r"   _ ╱ ", r" ╱ ◎^╲╲", r"│◎═╦═│", r" ╲☉─╲ ", r"  └┘  " ]  # UR
        ]
    },
    { # 2: Wagon
        "name": "Wagon",
        "hp": 120, "weight": 14, "drag": 0.05, "braking": 10, "turn_rate": 0.10,
        "durability": 90, "gas_capacity": 5500, "gas_consumption": 0.09,
        "attachment_points": {
            "roof_center": {"offset_x": 0, "offset_y": -1, "size": 2},
            "bumper": {"offset_x": 4, "offset_y": 0, "size": 1}
        },
        "mounted_weapons": {"roof_center": "lmg"},
        "ammo_bullet": 250, "ammo_heavy_bullet": 0, "ammo_fuel": 0,
        "inventory": [], # Initial inventory
        "menu_art": [
            r"  ╭──────────╮ ", r"╭─╢    ____    ╟─╮", r"│ │ ╱ ◎ ◎╲ │ │", r"╞═╧═╡------╞═╧═╡", r"╰─☉─┴──────┴─☉─╯",
        ],
        "art": [
            [ r" ╭─────────╮", r"╭╢    ____  ║", r"│║ ╱ ◎ ◎╲ ║", r"╞╧═╡─────>╞", r"╰─☉┴──────╯" ], # R
            [ r" ╭─────╮╱ ", r"╭╢ __ ◎║ ", r"│║╱ ◎ ◎║ ", r"╞╧═╡══V│ ", r"╰─☉┴───╯ " ], # DR
            [ r" ╭────────╮ ", r" │ □────□ │ ", r" │ ◎OOOO◎ │ ", r" │ V════V │ ", r" ╰─☉────☉─╯ " ], # D
            [ r" ╲╭─────╮ ", r"  ║◎ __ ╟╮", r"  ║ ◎ ◎╲║│", r"  │V══╞═╧╡", r"  ╰───┴☉─╯" ], # DL
            [ r" ╭─────────╮ ", r" ║  ____    ╟╮", r" ║ ╱ ◎ ◎╲ ║│", r" ╞<─────╞═╧╡", r" ╰──────┴☉─╯ " ], # L
            [ r" ╲ ╭───╮ ", r"  ║^ __ ╟╮", r"  ║ ◎ ◎╲║│", r"  │^══╞═╧╡", r"  ╰───┴☉─╯" ], # UL
            [ r" ╭────────╮ ", r" │ │────│ │ ", r" │ ◎OOOO◎ │ ", r" │ ^════^ │ ", r" ╰─☉────☉─╯ " ], # U
            [ r"  ╭───╮ ╱ ", r" ╭╢ __ ^║ ", r" │║╱ ◎ ◎║ ", r" ╞╧═╡^^ │ ", r" ╰─☉┴───╯ " ]  # UR
        ]
    },
    { # 3: Truck
        "name": "Truck",
        "hp": 150, "weight": 18, "drag": 0.07, "braking": 8, "turn_rate": 0.07,
        "durability": 120, "gas_capacity": 7000, "gas_consumption": 0.11,
        "attachment_points": {
            "bed_center": {"offset_x": -2, "offset_y": 0, "size": 2},
            "roof": {"offset_x": 0, "offset_y": -1, "size": 2},
            "bumper": {"offset_x": 4, "offset_y": 0, "size": 1}
        },
        "mounted_weapons": {"bed_center": "hmg"},
        "ammo_bullet": 0, "ammo_heavy_bullet": 100, "ammo_fuel": 0,
        "inventory": [], # Initial inventory
        "menu_art": [
            r"        ╭──────╮ ", r"     ╭─╢╱╲  ╱╲╟╮", r"    ╒═╡═ ◎  ◎ ╞═╕", r" ╱ ╘═╤══════╤═╛", r"│    │------│  ", r"╰☉───╧══════╧☉─╯",
        ],
        "art": [
            [ r"   ╭─────╮  ", r" ╭─╢╱╲ ╱╲║  ", r"╒═╡═ ◎ ◎ ║> ", r"│ ╘═╤═════╤═╗", r"╰☉─���╧═════╧☉╝" ], # R
            [ r"  ╭───╮ ", r" ╭╢╱╲◎║ ", r"╒═╡═◎◎║ ", r"│ ╘═╤V │ ", r"╰☉──╧══☉╝" ], # DR
            [ r" ╭──────╮ ", r" │ ◎  ◎ │ ", r" │██████│ ", r" │ V══V │ ", r"╔╧══════╧╗", r"╚☉──────☉╝" ], # D
            [ r"   ╭───╮ ", r"  ║◎╱╲╟╮ ", r"  ║◎◎═╞═╕ ", r"  │ V╤═╛ │ ", r" ╚☉══╧──☉╯ " ], # DL
            [ r"   ╭─────╮ ", r"  ║╱╲ ╱╲╟─╮", r" <║ ◎ ◎ ╞═╕", r"╔═╤═════╤═╛ │", r"╚☉╧═════╧──☉╯" ], # L
            [ r"   ╭───╮ ", r"  ║^╱╲╟╮ ", r"  ║◎◎═╞═╕ ", r"  │ ^╤═╛ │ ", r" ╚☉══╧──☉╯ " ], # UL
            [ r" ╭──────╮ ", r" │ │──│ │ ", r" │ ◎  ◎ │ ", r" │ ^══^ │ ", r"╔╧══════╧╗", r"╚☉──────☉╝" ], # U
            [ r"  ╭───╮ ", r" ╭╢╱╲^ ║ ", r"╒═╡═◎◎║ ", r"│ ╘═╤^ │ ", r"╰☉──╧══☉╝" ]  # UR
        ]
    },
    { # 4: Hotrod
        "name": "Hotrod",
        "hp": 250, "weight": 9, "drag": 0.06, "braking": 11, "turn_rate": 0.15,
        "durability": 50, "gas_capacity": 3500, "gas_consumption": 0.15,
        "attachment_points": {
            "engine_top": {"offset_x": 2, "offset_y": 0, "size": 2},
            "roof": {"offset_x": 0, "offset_y": -1, "size": 2},
            "bumper": {"offset_x": 4, "offset_y": 0, "size": 1}
        },
        "mounted_weapons": {"engine_top": "hmg"},
        "ammo_bullet": 0, "ammo_heavy_bullet": 80, "ammo_fuel": 0,
        "inventory": [], # Initial inventory
        "menu_art": [
            r"      ╭────╮    ",
            r"    ╱ ____ ╲    ",
            r" ╭╡ ◎!! ◎ ╞╮ ", # Exclamation marks for engine
            r" │ ╲____╱ │ ",
            r" ╰─☉────◎◎╯ ",
        ],
        "art": [
            [ r"   ╭────╮", r"  ╱ ____ ╲", r" ╞ ◎!! ◎═>>", r" │ ╲____╱ │", r" ╰─☉────◎◎╯" ], # R
            [ r"  ╭───╮ ", r" ╱__ ◎\\", r"╞ ◎=!!║ ", r"│ ╲__╱ │ ", r"╰─☉──◎╯ " ], # DR
            [ r" ╭──────╮ ", r"╱ ◎    ◎ ╲", r"│ | V!!V | │", r"│ ╲____╱ │", r" ╰☉────◎◎╯" ], # D
            [ r"  ╭───╮ ", r" //◎ __╲ ", r" ║!!=◎ ╞ ", r" │ ╲__╱ │ ", r" ╰◎───☉╯ " ], # DL
            [ r"   ╭────╮   ", r"  ╱ ____ ╲  ", r"<<═◎!! ◎ ╞╮ ", r" │ ╲____╱ │ ", r" ╰◎◎────☉╯ " ], # L
            [ r"  ╭───╮ ", r" //^ __╲ ", r" ║!!=◎ ╞ ", r" │ ╲__╱\\ ", r" ╰◎───☉╯ " ], # UL
            [ r" ╭──────╮ ", r"╱ \ ^ ^ /╲ ", r"│ | |!!| | │", r"│ ◎ |=| ◎ │", r" ╰☉────◎◎╯" ], # U
            [ r"  ╭───╮ ", r" //◎ __^\\", r" ║ ◎=!!╞ ", r" │ ╲__╱ │ ", r" ╰─☉──◎╯ " ]  # UR
        ]
    },
    { # 5: Minivan
        "name": "Minivan",
        "hp": 90, "weight": 16, "drag": 0.08, "braking": 9, "turn_rate": 0.08,
        "durability": 100, "gas_capacity": 6000, "gas_consumption": 0.07,
        "attachment_points": {
            "roof_center": {"offset_x": 0, "offset_y": -1, "size": 3},
            "right_side": {"offset_x": 0, "offset_y": 1, "size": 2},
            "bumper": {"offset_x": 4, "offset_y": 0, "size": 1}
        },
        "mounted_weapons": {"roof_center": "flamethrower", "right_side": "hmg"},
        "ammo_bullet": 0, "ammo_heavy_bullet": 50, "ammo_fuel": 300,
        "inventory": [], # Initial inventory
        "menu_art": [
            r"    ╭─────────╮    ", r" ╭─╢ □ □ □ □ ╟─╮ ", r" │ ╞═ ◎    ◎ ═╡ │ ", r" │ │ ║    ║ │ │ ", r" ╰─╧═╧═══╧═╧─╯ ", r"    ╰─☉────☉─╯    ",
        ],
        "art": [
            [ r"  ╭─────────╮ ", r" ╭╢ □ □ □ □ ║ ", r" │╞═ ◎    ◎ >║ ", r" ││ ║    ║ │ ║ ", r" ╰╧═╧═══╧═╧─╯ ", r"  ╰─☉─��──☉─╯  " ], # R
            [ r"  ╭───────╮ ", r" ╭╢ □ □ ◎ ║ ", r" │╞═ ◎ = ║ ", r" ││ ║ V ║ │ ", r" ╰╧═╧═══╧─╯ ", r"    ╰─☉───╯  " ], # DR
            [ r" ╭─────────╮ ", r" │ ◎       ◎ │ ", r" │█████████│ ", r" │ V═════V │ ", r" ╞═╧═════╧═╡ ", r" ╰─☉─────☉─╯ " ], # D
            [ r"  ╭───────╮ ", r"  ║ ◎ □ □ ╟╮ ", r"  ║ = ◎ ═╡│ ", r"  ║ │ V ║ ││ ", r"  ╰─╧═══╧═╧╯ ", r"    ╰───☉─╯  " ], # DL
            [ r"  ╭─────────╮ ", r"  ║ □ □ □ □ ╟╮ ", r"  ║< ◎    ◎ ═╡│ ", r"  ║ │ ║    ║ ││ ", r"  ╰─╧═╧═══╧═╧╯ ", r"    ╰─☉────☉─╯ " ], # L
            [ r"  ╭───────╮ ", r"  ║ ^ □ □ ╟╮ ", r"  ║ = ◎ ═╡│ ", r"  ║ │ ^ ║ ││ ", r"  ╰─╧═══╧═╧╯ ", r"    ╰──���☉─╯  " ], # UL
            [ r" ╭─────────╮ ", r" │ │───│ │ │ ", r" │ ◎       ◎ │ ", r" │ ^═════^ │ ", r" ╞═╧═════╧═╡ ", r" ╰─☉─────☉─╯ " ], # U
            [ r"  ╭───────╮ ", r" ╭╢ ◎ □ □^║ ", r" │╞═ = ◎ ║ ", r" ││ │ ^ ║ │ ", r" ╰╧═╧═══╧─╯ ", r"    ╰─☉───╯  " ]  # UR
        ]
    }
]
