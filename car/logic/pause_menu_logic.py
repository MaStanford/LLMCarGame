import curses
import sys
from ..logic.save_load import save_game
from ..ui.pause_menu import draw_pause_menu
from ..ui.notifications import add_notification

def handle_pause_menu(stdscr, game_state, color_pair_map):
    """Handles the pause menu logic."""
    if not game_state.actions["toggle_pause"]:
        return

    selected_pause_option = 0
    while True:
        draw_pause_menu(stdscr, selected_pause_option, color_pair_map)
        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected_pause_option = (selected_pause_option - 1) % 4
        elif key == curses.KEY_DOWN:
            selected_pause_option = (selected_pause_option + 1) % 4
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if selected_pause_option == 0:  # Resume
                break
            elif selected_pause_option == 1:  # Save Game
                save_game(game_state)
                add_notification("Game Saved!", color="MENU_HIGHLIGHT")
            elif selected_pause_option == 2:  # Main Menu
                game_state.game_over = True # A bit of a hack to exit to main menu
                break
            elif selected_pause_option == 3:  # Quit
                sys.exit(0)
        elif key == 27:  # ESC also resumes
            break
