import math

def angle_to_direction(angle_rad: float) -> str:
    """Converts an angle in radians to an 8-point compass direction string."""
    # The game considers 0 radians to be North.
    # The circle is divided into 8 slices of 45 degrees (pi/4 radians).
    directions = ["N", "NW", "W", "SW", "S", "SE", "E", "NE"]
    
    # Normalize angle to be between 0 and 2*pi
    angle_rad = angle_rad % (2 * math.pi)
    
    # We shift the angle by half a slice (pi/8) to align the boundaries
    # correctly with the compass directions.
    index = int(((angle_rad + math.pi / 8) / (math.pi / 4))) % 8
    
    return directions[index]
