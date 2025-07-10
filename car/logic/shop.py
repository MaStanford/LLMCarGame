from ..entities.weapon import Weapon
from ..ui.mechanic_shop import draw_attachment_management_menu

class Shop:
    def __init__(self, name, inventory):
        self.name = name
        self.inventory = inventory

    def buy(self, item_info, game_state, world, stdscr, color_map):
        """
        Handles the purchase of an item.
        item_info (dict): Contains item details like name, type, price.
        game_state (GameState): The current state of the game.
        """
        price = item_info.get("price", 0)
        if game_state.player_cash < price:
            return False  # Not enough cash

        item_type = item_info.get("type")
        
        # Based on item type, perform the specific action
        if item_type == "fuel":
            amount = item_info.get("amount", 0)
            if game_state.current_gas < game_state.gas_capacity:
                game_state.player_cash -= price
                game_state.current_gas = min(game_state.gas_capacity, game_state.current_gas + amount)
                return True
        elif item_type == "repair":
            amount = item_info.get("amount", 0)
            if game_state.current_durability < game_state.max_durability:
                game_state.player_cash -= price
                game_state.current_durability = min(game_state.max_durability, game_state.current_durability + amount)
                return True
        elif item_type == "ammo":
            ammo_type = item_info.get("ammo_type")
            amount = item_info.get("amount", 0)
            if ammo_type:
                game_state.player_cash -= price
                if ammo_type not in game_state.ammo_counts:
                    game_state.ammo_counts[ammo_type] = 0
                game_state.ammo_counts[ammo_type] += amount
                return True
        elif item_type == "weapon":
            game_state.player_cash -= price
            weapon_id = item_info.get("weapon_id")
            if weapon_id:
                game_state.player_inventory.append(Weapon(weapon_id))
            return True
        elif item_type == "purchase_attachment":
            draw_attachment_management_menu(stdscr, game_state, color_map, "purchase")
            return True
        elif item_type == "upgrade_attachment":
            draw_attachment_management_menu(stdscr, game_state, color_map, "upgrade")
            return True
        
        return False

    def sell(self, item_info, game_state, world):
        """
        Handles the selling of an item from the player's inventory.
        item_info (dict): The item to sell.
        game_state (GameState): The current state of the game.
        """
        # For now, only weapons can be sold from inventory
        if item_info in game_state.player_inventory:
            price = item_info.get("price", 0) # In a real scenario, sell price would be lower
            game_state.player_cash += price
            game_state.player_inventory.remove(item_info)
            return True
        return False
