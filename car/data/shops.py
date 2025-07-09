from .buildings import BUILDING_DATA

SHOP_DATA = {
    key: value for key, value in BUILDING_DATA.items() if "inventory" in value
}
