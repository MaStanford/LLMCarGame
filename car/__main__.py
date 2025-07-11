import curses
import sys
import traceback
import time
import argparse
import logging
from .game import main_game
from .data.game_constants import MIN_TERMINAL_WIDTH, MIN_TERMINAL_HEIGHT

def check_terminal_size():
    """Checks if the terminal size is sufficient for the game."""
    h, w = 0, 0
    try:
        stdscr = curses.initscr()
        h, w = stdscr.getmaxyx()
        curses.endwin()
    except curses.error:
        try:
            import os
            size = os.get_terminal_size()
            w, h = size.columns, size.lines
        except (OSError, ImportError):
            pass

    if w < MIN_TERMINAL_WIDTH or h < MIN_TERMINAL_HEIGHT:
        print(f"Terminal window too small. Minimum size is {MIN_TERMINAL_WIDTH}x{MIN_TERMINAL_HEIGHT}, current size is {w}x{h}.", file=sys.stderr)
        return False
    return True

def main():
    """Main entry point for the game."""
    parser = argparse.ArgumentParser(description="A terminal-based automotive RPG.")
    parser.add_argument("--log", action="store_true", help="Enable logging to game.log")
    args = parser.parse_args()

    if args.log:
        logging.basicConfig(filename='game.log', level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filemode='w')
    else:
        logging.disable(logging.CRITICAL)

    if not check_terminal_size():
        sys.exit(1)
        
    try:
        time.sleep(0.1)
        curses.wrapper(main_game, logging.getLogger())
    except curses.error as e:
        if 'curses' in sys.modules and hasattr(curses, 'endwin') and callable(curses.endwin):
            try:
                if not curses.isendwin():
                    curses.endwin()
            except Exception:
                pass
        print(f"\n[ERROR] A curses error occurred: {e}", file=sys.stderr)
        print("This can happen if the terminal window is too small, or if the", file=sys.stderr)
        print("terminal type is not supported. Try resizing your window or", file=sys.stderr)
        print("running in a different terminal.", file=sys.stderr)
        traceback.print_exc()
    except Exception as e:
        if 'curses' in sys.modules and hasattr(curses, 'endwin') and callable(curses.endwin):
            try:
                if not curses.isendwin():
                    curses.endwin()
            except Exception:
                pass
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        traceback.print_exc()
    finally:
        logging.shutdown()

if __name__ == "__main__":
    main()
