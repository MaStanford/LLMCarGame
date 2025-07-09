import curses
from .shop import Shop
from ..data.shops import SHOP_DATA
from ..data.game_constants import CITY_SPACING
from ..world.generation import get_buildings_in_city

def handle_shop_interaction(stdscr, game_state, world, color_pair_map):
    """Handles the player's interaction with shops."""
    if game_state.car_speed < 1.0 and game_state.shop_cooldown == 0:
        grid_x = round(game_state.car_world_x / CITY_SPACING)
        grid_y = round(game_state.car_world_y / CITY_SPACING)
        city_buildings = get_buildings_in_city(grid_x, grid_y)
        
        for building in city_buildings:
            if building['x'] <= game_state.car_world_x < building['x'] + building['w'] and \
               building['y'] <= game_state.car_world_y < building['y'] + building['h']:
                
                if building["type"] in SHOP_DATA:
                    shop_data = SHOP_DATA[building["type"]]
                    shop = Shop(shop_data["name"], shop_data["inventory"])
                    selected_item_index = 0
                    active_list = "shop"
                    
                    while True:
                        player_stats = {
                            "inventory": game_state.player_inventory,
                            "cash": game_state.player_cash,
                            "durability": game_state.current_durability,
                            "max_durability": game_state.max_durability,
                            "current_gas": game_state.current_gas,
                            "gas_capacity": game_state.gas_capacity
                        }
                        from ..ui.shop import draw_shop_menu
                        draw_shop_menu(stdscr, shop, player_stats, selected_item_index, active_list, color_pair_map)
                        
                        key = stdscr.getch()
                        if key == curses.KEY_UP:
                            if active_list == "shop":
                                selected_item_index = (selected_item_index - 1) % len(shop.inventory) if shop.inventory else 0
                            else:
                                selected_item_index = (selected_item_index - 1) % len(game_state.player_inventory) if game_state.player_inventory else 0
                        elif key == curses.KEY_DOWN:
                            if active_list == "shop":
                                selected_item_index = (selected_item_index + 1) % len(shop.inventory) if shop.inventory else 0
                            else:
                                selected_item_index = (selected_item_index + 1) % len(game_state.player_inventory) if game_state.player_inventory else 0
                        elif key == curses.KEY_LEFT:
                            active_list = "shop"
                            selected_item_index = 0
                        elif key == curses.KEY_RIGHT:
                            active_list = "player"
                            selected_item_index = 0
                        elif key == curses.KEY_ENTER or key in [10, 13]:
                            if active_list == "shop":
                                item_to_buy = shop.inventory[selected_item_index]
                                if game_state.player_cash >= item_to_buy["price"]:
                                    game_state.player_cash -= item_to_buy["price"]
                                    game_state.player_inventory.append({"type": "item", "name": item_to_buy["item"]})
                            else:
                                if game_state.player_inventory:
                                    item_to_sell = game_state.player_inventory[selected_item_index]
                                    game_state.player_cash += item_to_sell.get("price", 0)
                                    game_state.player_inventory.pop(selected_item_index)
                        elif key == 27: # ESC
                            game_state.shop_cooldown = 100
                            break
                    return True # Interaction happened
    return False # No interaction
