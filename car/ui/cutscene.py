import curses
import time
import random

def play_cutscene(stdscr, frames, delay):
    """Plays a simple cutscene."""
    for frame in frames:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        for i, line in enumerate(frame):
            stdscr.addstr(h // 2 - len(frame) // 2 + i, w // 2 - len(line) // 2, line)
        stdscr.refresh()
        time.sleep(delay)

def play_explosion_cutscene(stdscr, art, color_map):
    """Plays an explosion cutscene."""
    frames = []
    for i in range(5):
        frame = []
        for line in art:
            new_line = ""
            for char in line:
                if char != ' ':
                    new_line += random.choice(["*", "💥", "🔥"])
                else:
                    new_line += ' '
            frame.append(new_line)
        frames.append(frame)
    
    play_cutscene(stdscr, frames, 0.1)

def play_death_cutscene(stdscr, color_map):
    """Plays a death cutscene."""
    frames = [
        ["You Died"],
        ["Game Over"],
    ]
    play_cutscene(stdscr, frames, 1)

def draw_cutscene_modal(stdscr, text, color_map):
    """Draws a cutscene modal."""
    h, w = stdscr.getmaxyx()
    win_h = 5
    win_w = 40
    win_y = h - win_h - 1
    win_x = (w - win_w) // 2

    win = curses.newwin(win_h, win_w, win_y, win_x)
    win.box()
    win.addstr(2, (win_w - len(text)) // 2, text)
    win.refresh()
    time.sleep(2)


