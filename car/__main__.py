import argparse
import logging
from logging.handlers import RotatingFileHandler
from .app import CarApp

def main():
    """Main entry point for the game."""
    parser = argparse.ArgumentParser(description="A terminal-based automotive RPG.")
    parser.add_argument("--log", action="store_true", help="Enable logging to game.log")
    args = parser.parse_args()

    if args.log:
        logging.basicConfig(
            level=logging.INFO,
            handlers=[
                RotatingFileHandler('game.log', maxBytes=5*1024*1024, backupCount=1, mode='w')
            ],
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    app = CarApp()
    app.run()

if __name__ == "__main__":
    main()
