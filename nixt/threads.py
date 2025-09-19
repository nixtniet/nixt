# This file is placed in the Public Domain.


"runtime"


import logging
import queue
import threading
import time
import _thread


LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'warn': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}


class Thread(threading.Thread):

    def __init__(self, func, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, None, (), daemon=daemon)
        self.name      = kwargs.get("name", name(func))
        self.queue     = queue.Queue()
        self.result    = None
        self.starttime = time.time()
        self.stopped   = threading.Event()
        self.queue.put((func, args))

    def __iter__(self):
        return self

    def __next__(self):
        yield from dir(self)

    def join(self, timeout=None):
        result = None
        try:
            super().join(timeout)
            result = self.result
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()
        return result

    def run(self):
        func, args = self.queue.get()
        try:
            self.result = func(*args)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


def launch(func, *args, **kwargs):
    thread = Thread(func, *args, **kwargs)
    thread.start()
    return thread


def level(loglevel="debug"):
    if loglevel != "none":
        format_short = "%(asctime)-8s %(message)-71s"
        datefmt = "%H:%M:%S"
        logging.basicConfig(datefmt=datefmt, format=format_short, force=True)
        logging.getLogger().setLevel(LEVELS.get(loglevel))


def name(obj):
    typ = type(obj)
    if "__builtins__" in dir(typ):
        return obj.__name__
    if "__self__" in dir(obj):
        return f"{obj.__self__.__class__.__name__}.{obj.__name__}"
    if "__class__" in dir(obj) and "__name__" in dir(obj):
        return f"{obj.__class__.__name__}.{obj.__name__}"
    if "__class__" in dir(obj):
        return f"{obj.__class__.__module__}.{obj.__class__.__name__}"
    if "__name__" in dir(obj):
        return f"{obj.__class__.__name__}.{obj.__name__}"
    return ""


def __dir__():
    return (
        'Thread',
        'launch',
        'level',
        'name'
   )
