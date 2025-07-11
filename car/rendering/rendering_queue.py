import curses

class RenderingQueue:
    def __init__(self):
        self.queue = []

    def add(self, z, func, *args, **kwargs):
        self.queue.append((z, func, args, kwargs))

    def draw(self, stdscr):
        self.queue.sort(key=lambda item: item[0])
        for _, func, args, kwargs in self.queue:
            func(stdscr, *args, **kwargs)
        self.queue = []

rendering_queue = RenderingQueue()
