import curses
from ..ui.main_menu import draw_main_menu
from ..ui.load_game import draw_load_game_menu
from .save_load import get_save_files, load_game

def handle_main_menu(stdscr, audio_manager, color_map):
    """
    Handles the main menu loop, including New Game, Load Game, and Quit.
    Returns a tuple: (action, game_state)
    'action' can be 'new_game', 'load_game', or 'quit'.
    'game_state' is the loaded GameState object if 'load_game' is chosen, otherwise None.
    """
    selected_option = 0
    audio_manager.play_music("car/sounds/main_menu.mid")

    while True:
        main_menu_win = draw_main_menu(stdscr, selected_option, color_map)
        if main_menu_win is None:
            return 'quit', None

        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected_option = (selected_option - 1) % 4
        elif key == curses.KEY_DOWN:
            selected_option = (selected_option + 1) % 4
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if selected_option == 0:  # New Game
                audio_manager.stop_music()
                audio_manager.play_music("car/sounds/world.mid")
                return 'new_game', None
            elif selected_option == 1:  # Load Game
                save_files = get_save_files()
                if not save_files:
                    continue  # No save files, so just continue the main menu loop

                selected_save_option = 0
                while True:
                    load_game_win = draw_load_game_menu(stdscr, save_files, selected_save_option, color_map)
                    if load_game_win is None:
                        break  # User escaped load menu, go back to main menu

                    key = stdscr.getch()
                    if key == curses.KEY_UP:
                        selected_save_option = (selected_save_option - 1) % len(save_files)
                    elif key == curses.KEY_DOWN:
                        selected_save_option = (selected_save_option + 1) % len(save_files)
                    elif key == curses.KEY_ENTER or key in [10, 13]:
                        game_state = load_game(save_files[selected_save_option])
                        audio_manager.stop_music()
                        audio_manager.play_music("car/sounds/world.mid")
                        return 'load_game', game_state
                    elif key == 27:  # ESC
                        break  # Go back to main menu
            elif selected_option == 2:  # Settings
                # Placeholder for settings logic
                pass
            elif selected_option == 3:  # Quit
                return 'quit', None
