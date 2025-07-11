import curses

def draw_city_hall_menu(stdscr, menu_options, selected_option, game_state, color_map):
    """Draws the main menu for the City Hall, using a shop-like layout."""
    h, w = stdscr.getmaxyx()
    
    # Main window
    win = curses.newwin(h, w, 0, 0)
    win.bkgd(' ', color_map.get("DEFAULT", 0))
    win.erase()

    # Left column (options)
    left_w = w // 2
    left_win = win.derwin(h - 2, left_w - 1, 1, 1)
    left_win.box()
    left_win.addstr(1, (left_w - 11) // 2, "City Hall", curses.A_BOLD | curses.A_UNDERLINE)

    for i, option in enumerate(menu_options):
        y = i + 3
        x = (left_w - len(option)) // 2
        if i == selected_option:
            left_win.addstr(y, x, option, color_map.get("MENU_HIGHLIGHT", 0) | curses.A_BOLD)
        else:
            left_win.addstr(y, x, option, color_map.get("MENU_TEXT", 0))

    # Right column (player stats)
    right_w = w - left_w
    right_win = win.derwin(h - 2, right_w - 1, 1, left_w)
    right_win.box()
    right_win.addstr(1, (right_w - 11) // 2, "Your Stats", curses.A_BOLD | curses.A_UNDERLINE)
    
    from ..rendering.draw_utils import add_stat_line
    current_stat_y = 3
    add_stat_line(right_win, current_stat_y, 2, f"Cash: ${game_state.player_cash}", right_w - 4)
    current_stat_y += 1
    add_stat_line(right_win, current_stat_y, 2, f"Durability: {int(game_state.current_durability)}/{int(game_state.max_durability)}", right_w - 4)
    current_stat_y += 1
    add_stat_line(right_win, current_stat_y, 2, f"Fuel: {int(game_state.current_gas)}/{int(game_state.gas_capacity)}", right_w - 4)
    
    win.refresh()
    left_win.refresh()
    right_win.refresh()

def draw_town_info_dialog(stdscr, info_text, color_map):
    """Draws a dialog box with information about the town."""
    h, w = stdscr.getmaxyx()
    dialog_h = 10
    dialog_w = 60
    dialog_y = (h - dialog_h) // 2
    dialog_x = (w - dialog_w) // 2

    dialog_win = curses.newwin(dialog_h, dialog_w, dialog_y, dialog_x)
    dialog_win.bkgd(' ', color_map.get("MENU_TEXT", 0))
    dialog_win.box()

    title = "Town Information"
    dialog_win.addstr(1, (dialog_w - len(title)) // 2, title, curses.A_BOLD)
    
    # Wrap text
    words = info_text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 > dialog_w - 4:
            lines.append(current_line)
            current_line = word
        else:
            current_line += " " + word
    lines.append(current_line)

    for i, line in enumerate(lines):
        dialog_win.addstr(3 + i, 2, line.strip())

    dialog_win.refresh()

def draw_quest_briefing(stdscr, quest, color_map):
    """Draws the quest briefing screen and returns True if the quest is accepted."""
    h, w = stdscr.getmaxyx()
    stdscr.clear()
    stdscr.refresh()
    
    briefing_h = 20
    briefing_w = 60
    briefing_y = (h - briefing_h) // 2
    briefing_x = (w - briefing_w) // 2

    briefing_win = curses.newwin(briefing_h, briefing_w, briefing_y, briefing_x)
    briefing_win.keypad(True)
    briefing_win.bkgd(' ', color_map.get("MENU_TEXT", 0))
    briefing_win.box()

    title = "Contract Briefing"
    briefing_win.addstr(1, (briefing_w - len(title)) // 2, title, curses.A_BOLD)

    briefing_win.addstr(3, 2, f"GIVER: {quest.quest_giver_faction}")
    briefing_win.addstr(4, 2, f"TARGET: {quest.target_faction}")
    briefing_win.addstr(6, 2, "OBJECTIVE:")
    briefing_win.addstr(7, 4, quest.description)
    briefing_win.addstr(10, 2, "REWARDS:")
    briefing_win.addstr(11, 4, f"- Cash: {quest.rewards['cash']}")
    briefing_win.addstr(12, 4, f"- XP: {quest.rewards['xp']}")
    briefing_win.addstr(14, 2, "CONSEQUENCES:")
    briefing_win.addstr(15, 4, f"- {quest.quest_giver_faction} Reputation: +10")
    briefing_win.addstr(16, 4, f"- {quest.target_faction} Reputation: -15")

    options = ["Accept Contract", "Decline"]
    selected_option = 0
    while True:
        for i, option in enumerate(options):
            y = briefing_h - 3 + i
            x = (briefing_w - len(option)) // 2
            if i == selected_option:
                briefing_win.addstr(y, x, option, color_map.get("MENU_HIGHLIGHT", 0) | curses.A_BOLD)
            else:
                briefing_win.addstr(y, x, option, color_map.get("MENU_TEXT", 0))
        briefing_win.refresh()

        key = briefing_win.getch()
        if key == curses.KEY_UP:
            selected_option = (selected_option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected_option = (selected_option + 1) % len(options)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return selected_option == 0
