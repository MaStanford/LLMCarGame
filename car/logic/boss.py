class Boss:
    def __init__(self, boss_data):
        self.name = boss_data["name"]
        self.car = next((c for c in CARS_DATA if c["name"] == boss_data["car"]), None)
        self.hp_multiplier = boss_data["hp_multiplier"]
        self.x = 0
        self.y = 0
        self.hp = 0
        self.art = []
        self.width = 0
        self.height = 0
