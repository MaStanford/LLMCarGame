import curses
from ..common.utils import draw_box

def draw_shop_menu(stdscr, shop, player_stats, selected_item_index, active_list, color_map):
    h, w = stdscr.getmaxyx()
    stdscr.clear()

    # Title
    title = shop.name
    stdscr.addstr(1, (w - len(title)) // 2, title, curses.A_BOLD)

    # Shop Inventory
    shop_win_w = w // 2 - 2
    shop_win_h = h - 4
    shop_win = stdscr.derwin(shop_win_h, shop_win_w, 2, 1)
    draw_box(shop_win, "Shop Inventory")

    for i, item in enumerate(shop.inventory):
        item_text = f"{item['item']} - ${item['price']}"
        if active_list == "shop" and i == selected_item_index:
            shop_win.addstr(2 + i, 2, item_text, curses.A_REVERSE)
        else:
            shop_win.addstr(2 + i, 2, item_text)

    # Player Inventory
    player_win_w = w // 2 - 2
    player_win_h = (h - 4) // 2
    player_win = stdscr.derwin(player_win_h, player_win_w, 2, w // 2 + 1)
    draw_box(player_win, "Player Inventory")

    for i, item in enumerate(player_stats["inventory"]):
        item_text = f"{item['name']} - ${item.get('price', 0)}"
        if active_list == "player" and i == selected_item_index:
            player_win.addstr(2 + i, 2, item_text, curses.A_REVERSE)
        else:
            player_win.addstr(2 + i, 2, item_text)

    # Player Stats
    stats_win_w = w // 2 - 2
    stats_win_h = (h - 4) // 2
    stats_win = stdscr.derwin(stats_win_h, stats_win_w, 2 + player_win_h, w // 2 + 1)
    draw_box(stats_win, "Player Stats")
    
    stats_win.addstr(2, 2, f"Cash: ${player_stats['cash']}")
    stats_win.addstr(3, 2, f"Durability: {player_stats['durability']}/{player_stats['max_durability']}")
    stats_win.addstr(4, 2, f"Gas: {player_stats['current_gas']:.0f}/{player_stats['gas_capacity']}")

    # Instructions
    instructions = "Up/Down: Select | Left/Right: Switch | Enter: Buy/Sell | ESC: Exit"
    stdscr.addstr(h - 2, (w - len(instructions)) // 2, instructions)

    stdscr.refresh()
    shop_win.refresh()
    player_win.refresh()
    stats_win.refresh()
