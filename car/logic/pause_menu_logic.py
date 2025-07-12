import curses
import sys
from ..logic.save_load import save_game
from ..ui.pause_menu import draw_pause_menu
from ..ui.notifications import add_notification

def handle_pause_menu(stdscr, game_state, color_pair_map):
    """Handles the pause menu logic."""
    actions = game_state.actions

    if game_state.menu_nav_cooldown == 0:
        if actions["menu_up"]:
            game_state.selected_pause_option = (game_state.selected_pause_option - 1) % 4
            game_state.menu_nav_cooldown = 5
        elif actions["menu_down"]:
            game_state.selected_pause_option = (game_state.selected_pause_option + 1) % 4
            game_state.menu_nav_cooldown = 5

    if actions["menu_select"]:
        if game_state.selected_pause_option == 0:  # Resume
            game_state.pause_menu_open = False
        elif game_state.selected_pause_option == 1:  # Save Game
            save_game(game_state)
            add_notification("Game Saved!", color="MENU_HIGHLIGHT")
            game_state.pause_menu_open = False # Close menu after saving
        elif game_state.selected_pause_option == 2:  # Main Menu
            game_state.game_over = True 
            game_state.pause_menu_open = False
        elif game_state.selected_pause_option == 3:  # Quit
            sys.exit(0)
    elif actions["menu_back"]:
        game_state.pause_menu_open = False

