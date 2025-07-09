import curses
import sys
import traceback
import time
from .game import main_game
from .data.game_constants import MIN_TERMINAL_WIDTH, MIN_TERMINAL_HEIGHT

def check_terminal_size():
    """Checks if the terminal size is sufficient for the game."""
    h, w = 0, 0
    try:
        # Try to get size from curses
        stdscr = curses.initscr()
        h, w = stdscr.getmaxyx()
        curses.endwin()
    except curses.error:
        # Fallback for environments where curses is problematic
        try:
            import os
            size = os.get_terminal_size()
            w, h = size.columns, size.lines
        except (OSError, ImportError):
            pass # Unable to determine size

    if w < MIN_TERMINAL_WIDTH or h < MIN_TERMINAL_HEIGHT:
        print(f"Terminal window too small. Minimum size is {MIN_TERMINAL_WIDTH}x{MIN_TERMINAL_HEIGHT}, current size is {w}x{h}.", file=sys.stderr)
        return False
    return True

def main():
    """Main entry point for the game."""
    if not check_terminal_size():
        sys.exit(1)
    try:
        time.sleep(0.1)
        curses.wrapper(main_game)
    except curses.error as e:
        # It's possible endwin is already called by the wrapper on error
        if 'curses' in sys.modules and hasattr(curses, 'endwin') and callable(curses.endwin):
            try:
                if not curses.isendwin():
                    curses.endwin()
            except Exception as cleanup_e:
                # Log cleanup error if necessary, but don't obscure the original error
                pass
        print(f"\n[ERROR] A curses error occurred: {e}", file=sys.stderr)
        print("This can happen if the terminal window is too small, or if the", file=sys.stderr)
        print("terminal type is not supported. Try resizing your window or", file=sys.stderr)
        print("running in a different terminal.", file=sys.stderr)
        traceback.print_exc() # Optional: for debugging
    except Exception as e:
        # Ensure curses is cleaned up on any other exception
        if 'curses' in sys.modules and hasattr(curses, 'endwin') and callable(curses.endwin):
            try:
                if not curses.isendwin():
                    curses.endwin()
            except Exception as cleanup_e:
                pass # As above
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        traceback.print_exc()

if __name__ == "__main__":
    main()
