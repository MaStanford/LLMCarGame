import curses

def handle_input(stdscr, game_state):
    """Handles all user input for the game."""
    keys = set()
    key = stdscr.getch()
    while key != -1:
        keys.add(key)
        key = stdscr.getch()

    actions = {
        "accelerate": False,
        "brake": False,
        "turn_left": False,
        "turn_right": False,
        "fire": False,
        "toggle_menu": False,
        "toggle_pause": False,
        "menu_up": False,
        "menu_down": False,
        "menu_left": False,
        "menu_right": False,
        "menu_select": False,
        "menu_back": False,
        "quit": False,
    }

    if game_state.menu_open:
        if curses.KEY_UP in keys:
            actions["menu_up"] = True
        if curses.KEY_DOWN in keys:
            actions["menu_down"] = True
        if curses.KEY_LEFT in keys:
            actions["menu_left"] = True
        if curses.KEY_RIGHT in keys:
            actions["menu_right"] = True
        if curses.KEY_ENTER in keys or 10 in keys or 13 in keys:
            actions["menu_select"] = True
        if 27 in keys: # ESC
            actions["menu_back"] = True
    else:
        if ord('w') in keys or curses.KEY_UP in keys:
            actions["accelerate"] = True
        if ord('s') in keys or curses.KEY_DOWN in keys:
            actions["brake"] = True
        if ord('a') in keys or curses.KEY_LEFT in keys:
            actions["turn_left"] = True
        if ord('d') in keys or curses.KEY_RIGHT in keys:
            actions["turn_right"] = True
        if ord(' ') in keys:
            actions["fire"] = True
        if curses.KEY_ENTER in keys or 10 in keys or 13 in keys:
            actions["brake"] = True

    if 9 in keys: # TAB
        if game_state.menu_toggle_cooldown == 0:
            actions["toggle_menu"] = True
            game_state.menu_toggle_cooldown = 5 # 5 frames cooldown
    
    if 27 in keys: # ESC
        if game_state.menu_open:
            actions["toggle_menu"] = True
        else:
            actions["toggle_pause"] = True


    return actions
