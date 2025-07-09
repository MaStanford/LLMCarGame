import string

BUILDING_OUTLINE = { # Double line characters
    "topLeft": '╔', "topRight": '╗', "bottomLeft": '╚', "bottomRight": '╝',
    "vertical": '║', "horizontal": '═'
}
# Added more symbols, removed some confusing ones
BUILDING_NAME_CHARS = string.ascii_uppercase + string.digits + "!#$%&*+=?☆★♥♦♣♠♪♫☼►◄▲▼"
