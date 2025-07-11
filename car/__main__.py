import curses
import sys
import traceback
import time
import argparse
import logging
import os
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

    # Get the root logger
    logger = logging.getLogger()

    if args.log:
        # Clear any existing handlers
        if logger.hasHandlers():
            logger.handlers.clear()
        
        # Set the level for the root logger
        logger.setLevel(logging.INFO)
        
        # Create a file handler that overwrites the file and add it
        handler = logging.FileHandler('game.log', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
    else:
        # Disable all logging below CRITICAL level if --log is not set
        logging.disable(logging.CRITICAL)

    if not check_terminal_size():
        sys.exit(1)
        
    try:
        time.sleep(0.1)
        curses.wrapper(main_game, logger)
    except curses.error as e:
        if 'curses' in sys.modules and hasattr(curses, 'endwin') and callable(curses.endwin):
            try:
                if not curses.isendwin():
                    curses.endwin()
            except Exception:
                pass
        logger.error(f"A curses error occurred: {e}", exc_info=True)
        print(f"\n[ERROR] A curses error occurred: {e}", file=sys.stderr)
        print("This can happen if the terminal window is too small, or if the", file=sys.stderr)
        print("terminal type is not supported. Try resizing your window or", file=sys.stderr)
        print("running in a different terminal.", file=sys.stderr)
    except Exception as e:
        if 'curses' in sys.modules and hasattr(curses, 'endwin') and callable(curses.endwin):
            try:
                if not curses.isendwin():
                    curses.endwin()
            except Exception:
                pass
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        traceback.print_exc()
    finally:
        logging.shutdown()

if __name__ == "__main__":
    main()
