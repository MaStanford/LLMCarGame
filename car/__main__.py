import curses
import sys
import traceback
from .game import main_game

def main():
    """Main entry point for the game."""
    try:
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
        # traceback.print_exc() # Optional: for debugging
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
