import argparse
import logging
from logging import FileHandler
from .app import CarApp

def main():
    """Main entry point for the game."""
    parser = argparse.ArgumentParser(description="A terminal-based automotive RPG.")
    parser.add_argument("--log", action="store_true", help="Enable logging to game.log")
    parser.add_argument("--dev", action="store_true", help="Enable dev mode")
    args = parser.parse_args()

    if args.log:
        logging.basicConfig(
            level=logging.INFO,
            handlers=[
                FileHandler('game.log', mode='w')
            ],
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    app = CarApp()
    app.dev_mode = args.dev
    app.run()

if __name__ == "__main__":
    main()
