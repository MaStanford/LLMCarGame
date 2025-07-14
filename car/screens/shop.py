from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static
from ..widgets.weapon_info import WeaponInfo

class ShopScreen(ModalScreen):
    """The shop screen."""

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        yield Static("Item List", id="item_list")
        yield WeaponInfo(id="item_info")
        yield Static("Dialog Box", id="dialog_box")
        yield Footer()
