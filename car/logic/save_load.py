import pickle
import os

SAVE_DIR = "saves"

def save_game(game_state):
    """Saves the game state to a file."""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    
    save_files = sorted([f for f in os.listdir(SAVE_DIR) if f.endswith(".sav")], reverse=True)
    next_save_num = 1
    if save_files:
        try:
            next_save_num = int(save_files[0].replace("save", "").replace(".sav", "")) + 1
        except ValueError:
            pass # If the latest save file is not a number, we'll just use 1
            
    save_path = os.path.join(SAVE_DIR, f"save{next_save_num}.sav")
    
    with open(save_path, "wb") as f:
        pickle.dump(game_state, f)

def load_game(save_file):
    """Loads a game state from a file."""
    save_path = os.path.join(SAVE_DIR, save_file)
    with open(save_path, "rb") as f:
        return pickle.load(f)

def get_save_files():
    """Returns a list of save files."""
    if not os.path.exists(SAVE_DIR):
        return []
    return sorted([f for f in os.listdir(SAVE_DIR) if f.endswith(".sav")])
