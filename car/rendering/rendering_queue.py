import curses
import logging

class RenderingQueue:
    def __init__(self):
        self.queue = []

    def add(self, z, func, *args, **kwargs):
        logging.info(f"QUEUE_ADD: z={z}, func={func.__name__}, args_len={len(args)}, kwargs_keys={list(kwargs.keys())}")
        self.queue.append((z, func, args, kwargs))

    def draw(self, stdscr):
        logging.info(f"QUEUE_DRAW_START: Drawing {len(self.queue)} items.")
        self.queue.sort(key=lambda item: item[0])
        for z, func, args, kwargs in self.queue:
            try:
                # We can't log the full args because stdscr objects are not serializable
                logging.info(f"QUEUE_DRAW_ITEM: z={z}, func={func.__name__}")
                func(*args, **kwargs)
            except Exception as e:
                logging.error(f"QUEUE_DRAW_ERROR: z={z}, func={func.__name__}, error={e}", exc_info=True)
        logging.info(f"QUEUE_DRAW_END: Finished drawing. Clearing queue.")
        self.queue = []
        stdscr.refresh()

rendering_queue = RenderingQueue()
