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
    h, w = stdscr.getmaxyx()
    art_h = len(art)
    art_w = max(len(line) for line in art) if art_h > 0 else 0
    start_y = h // 2 - art_h // 2
    start_x = w // 2 - art_w // 2

    # Initial frame with the enemy art
    frames.append(art)

    # Transition frames
    for i in range(art_h * art_w // 2):
        new_art = [list(row) for row in frames[-1]]
        while True:
            rand_y = random.randint(0, art_h - 1)
            rand_x = random.randint(0, art_w - 1)
            if new_art[rand_y][rand_x] != ' ':
                new_art[rand_y][rand_x] = random.choice(["*", "💥", "🔥"])
                break
        frames.append(["".join(row) for row in new_art])

    # Final explosion frames
    for i in range(5):
        frame = []
        for _ in range(art_h):
            frame.append("".join(random.choice(["*", "💥", "🔥", " "]) for _ in range(art_w)))
        frames.append(frame)

    for frame in frames:
        stdscr.clear()
        for i, line in enumerate(frame):
            stdscr.addstr(start_y + i, start_x, line)
        stdscr.refresh()
        time.sleep(0.05)


def play_death_cutscene(stdscr, color_map):
    """Plays a death cutscene."""
    frames = [
        ["You Died"],
        ["Game Over"],
    ]
    play_cutscene(stdscr, frames, 1)

def draw_cutscene_modal(stdscr, title, text, color_map):
    """Draws a cutscene modal."""
    h, w = stdscr.getmaxyx()
    win_h = 7
    win_w = 40
    win_y = h - win_h - 1
    win_x = w - win_w - 1

    win = curses.newwin(win_h, win_w, win_y, win_x)
    win.bkgd(' ', color_map.get("MENU_BORDER", 0))
    win.box()
    win.addstr(1, (win_w - len(title)) // 2, title, curses.A_BOLD)
    win.addstr(3, (win_w - len(text)) // 2, text)

    win.refresh()
    time.sleep(2)
    win.clear()
    win.refresh()



