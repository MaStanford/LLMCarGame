import curses
import time

notifications = []

def add_notification(text, duration=3, color="DEFAULT"):
    """Adds a notification to the list."""
    notifications.append({
        "text": text,
        "duration": duration,
        "color": color,
        "start_time": time.time()
    })

def draw_notifications(stdscr, color_map):
    """Draws active notifications."""
    h, w = stdscr.getmaxyx()
    
    for i, notification in enumerate(notifications):
        if time.time() - notification["start_time"] > notification["duration"]:
            notifications.pop(i)
            continue
            
        text = notification["text"]
        color_pair_num = color_map.get(notification["color"], 0)
        
        stdscr.addstr(h - 2 - i, (w - len(text)) // 2, text, curses.color_pair(color_pair_num))
