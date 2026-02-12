"""
Reveal animation system for loading screens.

A target image (drawn from the same charset as the noise) is hidden behind
a field of random characters. A reveal zone fans out from a randomly chosen
origin. Inside that zone, each cell generates a random character every tick.
When a cell's random character happens to match the target image character,
the cell "locks" and stays frozen. Over several seconds the full image
crystallises out of the noise, holds, then a new image + pattern is chosen.
"""

import math
import random

# ── Character set ─────────────────────────────────────────────────────────
# Single-line + double-line box-drawing, block elements, fill patterns,
# heavy-line box-drawing, and rounded corners for organic curves.
ANIMATION_CHARS = "░▒▓█▄▀▌▐─│┌┐└┘├┤┬┴┼═║╔╗╚╝╠╣╦╩╬▤▥▦▧▨▩━┃┏┓┗┛┣┫┳┻╋╭╮╯╰"

# ── Target images ─────────────────────────────────────────────────────────
# Each image is a list of 8 strings (padded to 50 chars by the normaliser).
# Only characters from ANIMATION_CHARS are used; spaces are background
# (they never lock — the noise keeps churning behind them).
# All interior cells are filled so the completed image is clearly distinct
# from the surrounding noise.

_SKULL = [
    "                 ┏━━━━━━━━━━━━━━┓                 ",
    "               ╔═╝░░░░░░░░░░░░░░╚═╗               ",
    "               ║░░░░▓▓▓░░░░▓▓▓░░░░║               ",
    "               ║░░░░░░░░▄▄░░░░░░░░║               ",
    "                ╚╗░░┬┴┬┴░░┴┬┴┬░░╔╝                ",
    "                 ┗━━╩══╩━━╩══╩━━┛                 ",
    "                     ┃┃░░┃┃                       ",
    "                     ╰╯░░╰╯                       ",
]

_CAR_TOP = [
    "                    ╭━━━━━━╮                      ",
    "                  ╭━┫▓▓▓▓▓▓┣━╮                    ",
    "                  ▌░┃░░░░░░┃░▐                    ",
    "                ┏━┻━┻══════┻━┻━┓                  ",
    "                ┃░░░░░░░░░░░░░░┃                  ",
    "                ┗━┳━┳══════┳━┳━┛                  ",
    "                  ▌░┃░░░░░░┃░▐                    ",
    "                  ╰━┫▓▓▓▓▓▓┣━╯                    ",
]

_SHIELD = [
    "                   ┏━━━━━━━━━━┓                   ",
    "                   ┃░░░░░░░░░░┃                   ",
    "                   ┃░▒▒▓▓▓▓▒▒░┃                   ",
    "                   ┃░▒▓████▓▒░┃                   ",
    "                   ┃░▒▒▓▓▓▓▒▒░┃                   ",
    "                    ╚╗░░░░░░╔╝                    ",
    "                     ╰╮░░░░╭╯                     ",
    "                      ╰━━━━╯                      ",
]

_CROSSHAIR = [
    "                       ░┃░                        ",
    "                       ░┃░                        ",
    "              ┏━━┓░░░░░░┃░░░░░░┏━━┓               ",
    "              ┃░░┗━━━━━━╋━━━━━━┛░░┃               ",
    "              ┃░░┏━━━━━━╋━━━━━━┓░░┃               ",
    "              ┗━━┛░░░░░░┃░░░░░░┗━━┛               ",
    "                       ░┃░                        ",
    "                       ░┃░                        ",
]

_MAZE = [
    "          ┏━━━┳━━━╦━━━╦━━━┳━━━┳━━━┓              ",
    "          ┃░░░┃░░░║░░░░░░░║░░░┃░░░┃              ",
    "          ┃░╔═┛░░░╚═╗░╔═══╝░░░┗━╗░┃              ",
    "          ┃░║░░░░░░░║░║░░░░░░░░░║░┃              ",
    "          ┃░╚═══╗░╔═╝░╚═══╗░╔═══╝░┃              ",
    "          ┃░░░░░║░║░░░░░░░║░║░░░░░┃              ",
    "          ┣━━━╗░║░╚═══╦═══╝░╚═╗░┏━┫              ",
    "          ┗━━━┻━┻═════╩═══════┻━┻━┛              ",
]

_RADIATION = [
    "                     ┏━━┓                         ",
    "                   ╔═╝▓▓╚═╗                       ",
    "                 ╔═╝▓▓▓▓▓▓╚═╗                     ",
    "               ━━╝░░░░▓▓░░░░╚━━                   ",
    "               ━━╗░░░░▓▓░░░░╔━━                   ",
    "                 ╚═╗▓▓▓▓▓▓╔═╝                     ",
    "                   ╚═╗▓▓╔═╝                       ",
    "                     ┗━━┛                         ",
]

_GAS_PUMP = [
    "                  ┏━━━━━━━━━━━━┓                  ",
    "                  ┃▒▒▒▒▒▒▒▒▒▒▒▒┃                  ",
    "                  ┃▒┏━━━━━━━━┓▒┃                  ",
    "                  ┃▒┃░░░░░░░░┃▒┃                  ",
    "                  ┃▒┗━━━━━━━━┛▒┃                  ",
    "                  ┃▒▒▒▒▒▒▒▒▒▒▒▒┃                  ",
    "                  ┗━━━━━┳┳━━━━━┛                  ",
    "                  ░░━━━━┛┗━━━━░░                  ",
]

_SWORD = [
    "                      ╭━━━╮                       ",
    "                      ┃▒▓▒┃                       ",
    "                      ┃▒▓▒┃                       ",
    "                      ┃▒▓▒┃                       ",
    "                    ╭━┫▒▓▒┣━╮                     ",
    "                    ┃░┗━━━┛░┃                     ",
    "                    ╰━╮░█░╭━╯                     ",
    "                      ╰━━━╯                       ",
]

_CITY = [
    "              ░░░░┏┓░░░░░░░░░░░░░░░░░░            ",
    "              ░░░░┃┃░░░░┏━━━┓░░░░░░░░░            ",
    "              ┏━┓░┃┃░░░░┃░░░┃░░░┏━━┓░░            ",
    "              ┃░┃░┃┃░┏┓░┃░░░┃░░░┃░░┃░░            ",
    "              ┃░┃░┃┃░┃┃░┃░░░┃░┏┓┃░░┃░░            ",
    "              ┃░┃░┃┃░┃┃░┃░░░┃░┃┃┃░░┃░░            ",
    "              ┃░┃░┃┃░┃┃░┃░░░┃░┃┃┃░░┃░░            ",
    "              ┻━┻━┻┻━┻┻━┻━━━┻━┻┻┻━━┻━━            ",
]

_LIGHTNING = [
    "                       ░░┏━━━┓                    ",
    "                     ░░┏━┛░░░┃                    ",
    "                   ░░┏━┛░░░░░┃                    ",
    "                   ┏━┛░░░░░░░┃                    ",
    "                   ┃░░░░░░░┏━┛░░                  ",
    "                   ┃░░░░░┏━┛░░                    ",
    "                   ┃░░░┏━┛░░                      ",
    "                   ┗━━━┛░░                        ",
]

REVEAL_IMAGES = [
    _SKULL, _CAR_TOP, _SHIELD, _CROSSHAIR, _MAZE,
    _RADIATION, _GAS_PUMP, _SWORD, _CITY, _LIGHTNING,
]

# Normalise: pad every row to exactly 50 chars with trailing spaces.
_IMG_WIDTH = 50
REVEAL_IMAGES = [
    [row.ljust(_IMG_WIDTH)[:_IMG_WIDTH] for row in img]
    for img in REVEAL_IMAGES
]


# ── Fan-out patterns ───────────────────────────────────────────────────────

def _dist_euclidean(x, y, ox, oy, aspect=6.0):
    """Euclidean distance with aspect-ratio correction.
    Terminal cells are roughly 2:1 tall-to-wide, so vertical distance is
    scaled up to make the reveal look circular rather than squished."""
    return math.sqrt((x - ox) ** 2 + ((y - oy) * aspect) ** 2)


def _make_pattern(name, width, height):
    """Return (origin, distance_func) for a named fan-out pattern."""
    mid_x, mid_y = width // 2, height // 2

    if name == "center":
        return lambda x, y: _dist_euclidean(x, y, mid_x, mid_y)
    elif name == "top_left":
        return lambda x, y: _dist_euclidean(x, y, 0, 0)
    elif name == "top_right":
        return lambda x, y: _dist_euclidean(x, y, width - 1, 0)
    elif name == "bottom_left":
        return lambda x, y: _dist_euclidean(x, y, 0, height - 1)
    elif name == "bottom_right":
        return lambda x, y: _dist_euclidean(x, y, width - 1, height - 1)
    elif name == "left":
        return lambda x, y: float(x)
    elif name == "right":
        return lambda x, y: float(width - 1 - x)
    elif name == "top":
        return lambda x, y: float(y) * 6.0
    elif name == "bottom":
        return lambda x, y: float(height - 1 - y) * 6.0
    elif name == "edges_in":
        return lambda x, y: float(min(x, width - 1 - x, y * 6, (height - 1 - y) * 6))

    # Fallback
    return lambda x, y: _dist_euclidean(x, y, mid_x, mid_y)


PATTERN_NAMES = [
    "center", "top_left", "top_right", "bottom_left", "bottom_right",
    "left", "right", "top", "bottom", "edges_in",
]


# ── RevealAnimation class ─────────────────────────────────────────────────

class RevealAnimation:
    """Manages the reveal-crystallisation animation loop."""

    def __init__(self, width=50, height=8):
        self.width = width
        self.height = height
        self.chars = ANIMATION_CHARS
        self._char_count = len(self.chars)
        self.reset()

    def reset(self):
        """Pick a new random image + fan-out pattern and clear all state."""
        self.target = random.choice(REVEAL_IMAGES)
        pattern_name = random.choice(PATTERN_NAMES)
        self.dist_fn = _make_pattern(pattern_name, self.width, self.height)

        # Pre-compute the maximum distance for this pattern so we know
        # how fast to grow the reveal radius.
        max_d = 0.0
        for y in range(self.height):
            for x in range(self.width):
                d = self.dist_fn(x, y)
                if d > max_d:
                    max_d = d
        # We want the zone to cover everything in ~2.5 seconds (50 ticks).
        self.reveal_speed = max(max_d / 50.0, 0.5)

        self.locked = [[False] * self.width for _ in range(self.height)]
        self.activation_tick = [[-1] * self.width for _ in range(self.height)]
        self.reveal_radius = 0.0
        self.tick_count = 0
        self.phase = "revealing"
        self.hold_ticks = 0

    def tick(self) -> str:
        """Advance one frame and return the rendered string."""
        if self.phase == "revealing":
            self._tick_reveal()
        elif self.phase == "holding":
            self.hold_ticks += 1
            if self.hold_ticks >= 60:  # 3 seconds at 50ms
                self.reset()

        return self._render()

    def _tick_reveal(self):
        """Expand the reveal zone and try to lock cells."""
        self.tick_count += 1
        self.reveal_radius += self.reveal_speed

        all_image_cells_locked = True

        for y in range(self.height):
            row_target = self.target[y]
            for x in range(self.width):
                if self.locked[y][x]:
                    continue

                target_char = row_target[x] if x < len(row_target) else " "

                # Space cells are background — they never lock.
                if target_char == " ":
                    continue

                all_image_cells_locked = False

                dist = self.dist_fn(x, y)
                if dist > self.reveal_radius:
                    continue

                # Cell just entered the active zone — record when.
                if self.activation_tick[y][x] < 0:
                    self.activation_tick[y][x] = self.tick_count

                # Match probability increases over time so stragglers resolve.
                ticks_active = self.tick_count - self.activation_tick[y][x]
                match_chance = (1.0 / self._char_count) + ticks_active * 0.003

                if random.random() < match_chance:
                    self.locked[y][x] = True

        if all_image_cells_locked:
            self.phase = "holding"
            self.hold_ticks = 0

    def _render(self) -> str:
        """Build the display string for this frame."""
        lines = []
        for y in range(self.height):
            row_target = self.target[y]
            line_chars = []
            for x in range(self.width):
                if self.locked[y][x]:
                    line_chars.append(row_target[x])
                else:
                    line_chars.append(random.choice(self.chars))
            lines.append("".join(line_chars))
        return "\n".join(lines)
