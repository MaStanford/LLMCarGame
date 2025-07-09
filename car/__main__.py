import curses
import sys
import traceback
from .game import main_game

def main():
    """Main entry point for the game."""
    try:
        curses.wrapper(main_game)
        print("Game exited normally.")
    except curses.error as e:
        if 'curses' in sys.modules and hasattr(curses, 'endwin') and callable(curses.endwin):
            try:
                if curses.isendwin() is False: curses.endwin()
            except Exception as cleanup_e:
                print(f"Error during manual curses cleanup: {cleanup_e}", file=sys.stderr)
        print(f"\nCurses error occurred: {e}", file=sys.stderr)
        print("Terminal might be too small, incompatible, or lack color/Unicode support.", file=sys.stderr)
        traceback.print_exc()
    except Exception as e:
        if 'curses' in sys.modules and hasattr(curses, 'endwin') and callable(curses.endwin):
            try:
                if curses.isendwin() is False: curses.endwin()
            except Exception as cleanup_e:
                print(f"Error during manual curses cleanup: {cleanup_e}", file=sys.stderr)
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        traceback.print_exc()

if __name__ == "__main__":
    main()
