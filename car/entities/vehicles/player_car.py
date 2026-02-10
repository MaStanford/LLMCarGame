from ..vehicle import Vehicle
from ..base import Entity

class PlayerCar(Vehicle):
    def __init__(self, x, y, art, durability, speed, acceleration, handling, braking_power, attachment_points, default_weapons={}, weapon_aim_speed=1.0):
        super().__init__(x, y, art, durability, speed, acceleration, handling)
        self.braking_power = braking_power
        self.weapon_aim_speed = weapon_aim_speed
        self.attachment_points = attachment_points
        self.default_weapons = default_weapons
        self.height, self.width = Entity.get_car_dimensions(list(art.values()))

    def update(self, game_state, world, dt):
        # Player car update logic is handled in the main game loop
        pass

    def get_art_for_angle(self, angle):
        """Gets the correct vehicle art for a given angle."""
        if isinstance(self.art, dict):
            angle = angle % 360
            if 337.5 <= angle or angle < 22.5:
                direction = "N"
            elif 22.5 <= angle < 67.5:
                direction = "NE"
            elif 67.5 <= angle < 112.5:
                direction = "E"
            elif 112.5 <= angle < 157.5:
                direction = "SE"
            elif 157.5 <= angle < 202.5:
                direction = "S"
            elif 202.5 <= angle < 247.5:
                direction = "SW"
            elif 247.5 <= angle < 292.5:
                direction = "W"
            else:
                direction = "NW"
            return self.art.get(direction, [""])
        return self.art

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        # The player car is drawn in the main render loop, so this can be empty
        pass
