import curses
import logging
import textwrap
from ..common.utils import draw_box
from ..rendering.draw_utils import add_stat_line
from ..rendering.rendering_queue import rendering_queue

def draw_city_hall_menu(stdscr, menu_options, selected_option, game_state, color_map):
    """Draws the main menu for the City Hall, using a shop-like layout."""
    h, w = stdscr.getmaxyx()
    
    # Left column (options)
    left_w = w // 2
    left_x = 1
    left_y = 1
    draw_box(stdscr, left_y, left_x, h - 2, left_w - 1, "City Hall", z_index=20)

    for i, option in enumerate(menu_options):
        y = left_y + i + 3
        x = left_x + (left_w - len(option)) // 2
        if i == selected_option:
            rendering_queue.add(21, stdscr.addstr, y, x, option, color_map.get("MENU_HIGHLIGHT", 0) | curses.A_BOLD)
        else:
            rendering_queue.add(21, stdscr.addstr, y, x, option, color_map.get("MENU_TEXT", 0))

    # Right column (player stats)
    right_w = w - left_w
    right_x = left_w
    right_y = 1
    draw_box(stdscr, right_y, right_x, h - 2, right_w - 1, "Your Stats", z_index=20)
    
    current_stat_y = right_y + 3
    add_stat_line(stdscr, current_stat_y, right_x + 2, "Cash", f"${game_state.player_cash}", color_map.get("MENU_TEXT", 0), z_index=21)
    current_stat_y += 1
    add_stat_line(stdscr, current_stat_y, right_x + 2, "Durability", f"{int(game_state.current_durability)}/{int(game_state.max_durability)}", color_map.get("MENU_TEXT", 0), z_index=21)
    current_stat_y += 1
    add_stat_line(stdscr, current_stat_y, right_x + 2, "Fuel", f"{int(game_state.current_gas)}/{int(game_state.gas_capacity)}", color_map.get("MENU_TEXT", 0), z_index=21)

def draw_quest_briefing(stdscr, quest, color_map):
    """Draws the quest briefing screen and returns True if the quest is accepted."""
    h, w = stdscr.getmaxyx()
    
    briefing_h = 20
    briefing_w = 60
    briefing_y = (h - briefing_h) // 2
    briefing_x = (w - briefing_w) // 2

    draw_box(stdscr, briefing_y, briefing_x, briefing_h, briefing_w, "Contract Briefing", z_index=30)

    rendering_queue.add(31, stdscr.addstr, briefing_y + 3, briefing_x + 2, f"GIVER: {quest.quest_giver_faction}", color_map.get("MENU_TEXT", 0))
    rendering_queue.add(31, stdscr.addstr, briefing_y + 4, briefing_x + 2, f"TARGET: {quest.target_faction}", color_map.get("MENU_TEXT", 0))
    rendering_queue.add(31, stdscr.addstr, briefing_y + 6, briefing_x + 2, "OBJECTIVE:", color_map.get("MENU_TEXT", 0))
    
    wrapped_description = textwrap.wrap(quest.description, briefing_w - 6)
    for i, line in enumerate(wrapped_description):
        rendering_queue.add(31, stdscr.addstr, briefing_y + 7 + i, briefing_x + 4, line, color_map.get("MENU_TEXT", 0))

    rendering_queue.add(31, stdscr.addstr, briefing_y + 10, briefing_x + 2, "REWARDS:", color_map.get("MENU_TEXT", 0))
    rendering_queue.add(31, stdscr.addstr, briefing_y + 11, briefing_x + 4, f"- Cash: {quest.rewards['cash']}", color_map.get("MENU_TEXT", 0))
    rendering_queue.add(31, stdscr.addstr, briefing_y + 12, briefing_x + 4, f"- XP: {quest.rewards['xp']}", color_map.get("MENU_TEXT", 0))
    rendering_queue.add(31, stdscr.addstr, briefing_y + 14, briefing_x + 2, "CONSEQUENCES:", color_map.get("MENU_TEXT", 0))
    rendering_queue.add(31, stdscr.addstr, briefing_y + 15, briefing_x + 4, f"- {quest.quest_giver_faction} Reputation: +10", color_map.get("MENU_TEXT", 0))
    rendering_queue.add(31, stdscr.addstr, briefing_y + 16, briefing_x + 4, f"- {quest.target_faction} Reputation: -15", color_map.get("MENU_TEXT", 0))

    options = ["Accept Contract", "Decline"]
    selected_option = 0
    while True:
        for i, option in enumerate(options):
            y = briefing_y + briefing_h - 3 + i
            x = briefing_x + (briefing_w - len(option)) // 2
            if i == selected_option:
                rendering_queue.add(31, stdscr.addstr, y, x, option, color_map.get("MENU_HIGHLIGHT", 0) | curses.A_BOLD)
            else:
                rendering_queue.add(31, stdscr.addstr, y, x, option, color_map.get("MENU_TEXT", 0))
        
        rendering_queue.draw(stdscr)
        
        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected_option = (selected_option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected_option = (selected_option + 1) % len(options)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return selected_option == 0
        elif key == 27:
            return False
