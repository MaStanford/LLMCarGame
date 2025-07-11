import curses
import logging
from ..common.utils import draw_box
from ..rendering.draw_utils import draw_weapon_stats_modal, add_stat_line
from ..rendering.rendering_queue import rendering_queue

def draw_shop_menu(stdscr, shop, player_stats, selected_item_index, active_list, color_map):
    h, w = stdscr.getmaxyx()
    
    # Title
    title = shop.name
    rendering_queue.add(10, stdscr.addstr, 1, (w - len(title)) // 2, title, curses.A_BOLD)

    # Shop Inventory
    shop_win_w = w // 2 - 2
    shop_win_h = h - 4
    shop_win_x = 1
    shop_win_y = 2
    draw_box(stdscr, shop_win_y, shop_win_x, shop_win_h, shop_win_w, "Shop Inventory", z_index=20)

    for i, item in enumerate(shop.inventory):
        item_text = f"{item['name']} - ${item['price']}"
        if active_list == "shop" and i == selected_item_index:
            rendering_queue.add(21, stdscr.addstr, shop_win_y + 2 + i, shop_win_x + 2, item_text, color_map.get("MENU_HIGHLIGHT", 0) | curses.A_BOLD)
            if item.get('type') == 'weapon':
                draw_weapon_stats_modal(stdscr, shop_win_y + 2 + i, shop_win_x + shop_win_w + 2, 10, 40, item['item'], color_map.get("MENU_TEXT", 0), z_index=30)
        else:
            rendering_queue.add(21, stdscr.addstr, shop_win_y + 2 + i, shop_win_x + 2, item_text, color_map.get("MENU_TEXT", 0))

    # Player Inventory
    player_win_w = w // 2 - 2
    player_win_h = (h - 4) // 2
    player_win_x = w // 2 + 1
    player_win_y = 2
    draw_box(stdscr, player_win_y, player_win_x, player_win_h, player_win_w, "Player Inventory", z_index=20)

    for i, item in enumerate(player_stats["inventory"]):
        item_text = f"{item.get('name')} - ${item.get('price', 0)}"
        if active_list == "player" and i == selected_item_index:
            rendering_queue.add(21, stdscr.addstr, player_win_y + 2 + i, player_win_x + 2, item_text, color_map.get("MENU_HIGHLIGHT", 0) | curses.A_BOLD)
            if item.get('type') == 'weapon':
                draw_weapon_stats_modal(stdscr, player_win_y + 2 + i, player_win_x + player_win_w + 2, 10, 40, item, color_map.get("MENU_TEXT", 0), z_index=30)
        else:
            rendering_queue.add(21, stdscr.addstr, player_win_y + 2 + i, player_win_x + 2, item_text, color_map.get("MENU_TEXT", 0))

    # Player Stats
    stats_win_w = w // 2 - 2
    stats_win_h = (h - 4) // 2
    stats_win_x = w // 2 + 1
    stats_win_y = 2 + player_win_h
    draw_box(stdscr, stats_win_y, stats_win_x, stats_win_h, stats_win_w, "Player Stats", z_index=20)
    
    add_stat_line(stdscr, stats_win_y + 2, stats_win_x + 2, "Cash", f"${player_stats['cash']}", color_map.get("MENU_TEXT", 0), z_index=21)
    add_stat_line(stdscr, stats_win_y + 3, stats_win_x + 2, "Durability", f"{player_stats['durability']}/{player_stats['max_durability']}", color_map.get("MENU_TEXT", 0), z_index=21)
    add_stat_line(stdscr, stats_win_y + 4, stats_win_x + 2, "Gas", f"{player_stats['current_gas']:.0f}/{player_stats['gas_capacity']}", color_map.get("MENU_TEXT", 0), z_index=21)

    # Instructions
    instructions = "Up/Down: Select | Left/Right: Switch | Enter: Buy/Sell | ESC: Exit"
    rendering_queue.add(10, stdscr.addstr, h - 2, (w - len(instructions)) // 2, instructions)
