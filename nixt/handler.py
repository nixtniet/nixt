# This file is placed in the Public Domain.


"event handler"


import logging
import queue
import threading
import time
import _thread


STARTTIME = time.time()


LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'warn': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}


class Event:

    def __init__(self):
        self._ready = threading.Event()
        self._thr = None
        self.args = []
        self.channel = ""
        self.ctime = time.time()
        self.rest = ""
        self.result = {}
        self.txt = ""
        self.type = "event"

    def done(self):
        self.reply("ok")

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result[time.time()] = txt

    def wait(self, timeout=None):
        try:
            self._ready.wait()
            if self._thr:
                self._thr.join()
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


class Handler:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()
        self.ready = threading.Event()
        self.stopped = threading.Event()

    def available(self, event):
        return event.type in self.cbs

    def callback(self, event):
        func = self.cbs.get(event.type, None)
        if func:
            event._thr = launch(func, event)

    def loop(self):
        while not self.stopped.is_set():
            try:
                event = self.poll()
                if event is None or self.stopped.is_set():
                    break
                event.orig = repr(self)
                self.callback(event)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    def poll(self):
        return self.queue.get()

    def put(self, event):
        self.queue.put(event)

    def register(self, typ, cbs):
        self.cbs[typ] = cbs

    def start(self, daemon=True):
        self.stopped.clear()
        launch(self.loop, daemon=daemon)

    def stop(self):
        self.stopped.set()
        self.queue.put(None)

    def wait(self):
        pass


class Task(threading.Thread):

    def __init__(self, func, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, None, (), daemon=daemon)
        self.name = kwargs.get("name", name(func))
        self.queue = queue.Queue()
        self.result = None
        self.starttime = time.time()
        self.stopped = threading.Event()
        self.queue.put((func, args))

    def __iter__(self):
        return self

    def __next__(self):
        yield from dir(self)

    def run(self):
        func, args = self.queue.get()
        try:
            self.result = func(*args)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()

    def join(self, timeout=None):
        try:
            super().join(timeout)
            return self.result
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def launch(func, *args, **kwargs):
    thread = Task(func, *args, **kwargs)
    thread.start()
    return thread


def level(loglevel="debug"):
    if loglevel != "none":
        format_short = "%(message)-80s"
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


def rlog(loglevel, txt, ignore=None):
    if ignore is None:
        ignore = []
    for ign in ignore:
        if ign in str(txt):
            return
    logging.log(LEVELS.get(loglevel), txt)


def __dir__():
    return (
        'STARTTIME',
        'Event',
        'Handler'
        'Repeater',
        'Task',
        'Timed'
        'launch',
        'level',
        'name',
        'rlog',
   )
