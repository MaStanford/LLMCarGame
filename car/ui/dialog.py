import curses

def draw_dialog_modal(stdscr, text_lines):
    """
    Draws a non-blocking dialog modal in the bottom-left corner of the screen.
    """
    h, w = stdscr.getmaxyx()
    modal_h = len(text_lines) + 2
    modal_w = max(len(line) for line in text_lines) + 4
    modal_y = h - modal_h - 1
    modal_x = 1

    modal_win = curses.newwin(modal_h, modal_w, modal_y, modal_x)
    modal_win.box()

    for i, line in enumerate(text_lines):
        modal_win.addstr(i + 1, 2, line)

    modal_win.addstr(modal_h - 1, 2, "(Press any key to continue)")
    modal_win.refresh()
