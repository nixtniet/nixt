# This file is placed in the Public Domain.
# pylint: disable=R0902


"runtime"


import logging
import queue
import threading
import time
import _thread


LEVELS = {
    'debug'   : logging.DEBUG,
    'info'    : logging.INFO,
    'warning' : logging.WARNING,
    'warn'    : logging.WARNING,
    'error'   : logging.ERROR,
    'critical': logging.CRITICAL,
}


class Event:

    "Event"

    def __init__(self):
        self._ready  = threading.Event()
        self._thr    = None
        self.args    = []
        self.channel = ""
        self.ctime   = time.time()
        self.orig    = ""
        self.rest    = ""
        self.result  = {}
        self.txt     = ""
        self.type    = "event"

    def done(self):
        "echo done reply."
        self.reply("ok")

    def ready(self):
        "flag event as ready."
        self._ready.set()

    def reply(self, txt):
        "add txt to result."
        self.result[time.time()] = txt

    def wait(self, timeout=None):
        "wait for event to finish."
        try:
            self._ready.wait()
            if self._thr:
                self._thr.join(timeout)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


class Handler:

    "handler"

    def __init__(self):
        self.cbs     = {}
        self.queue   = queue.Queue()
        self.ready   = threading.Event()
        self.stopped = threading.Event()

    def available(self, event):
        "check whether callback for event is there."
        return event.type in self.cbs

    def callback(self, event):
        "handle callbacks for event."
        func = self.cbs.get(event.type, None)
        if func:
            event._thr = launch(func, event, name=event.txt and event.txt.split()[0]) # pylint: disable=W0212
        else:
            event.ready()

    def loop(self):
        "callback loop."
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
        "poll for event."
        return self.queue.get()

    def put(self, event):
        "put event onto the queue."
        self.queue.put(event)

    def register(self, typ, cbs):
        "register callback."
        self.cbs[typ] = cbs

    def start(self, daemon=True):
        "start handler."
        self.stopped.clear()
        launch(self.loop, daemon=daemon)

    def stop(self):
        "stop handler."
        self.stopped.set()
        self.queue.put(None)


class Thread(threading.Thread):

    "thread"

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
        "join thread and return result."
        result = None
        try:
            super().join(timeout)
            result = self.result
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()
        return result

    def run(self):
        "run thread."
        func, args = self.queue.get()
        try:
            self.result = func(*args)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()
        except Exception as ex: # pylint: disable=W0718
            logging.exception(ex)
            _thread.interrupt_main()


class Timy(threading.Timer):

    "timy"

    def __init__(self, sleep, func, *args, **kwargs):
        super().__init__(sleep, func)
        self.name  = kwargs.get("name", name(func))
        self.sleep = sleep
        self.state = {}
        self.state["latest"] = time.time()
        self.state["starttime"] = time.time()
        self.starttime = time.time()


class Timed:

    "timed"

    def __init__(self, sleep, func, *args, thrname="", **kwargs):
        self.args   = args
        self.func   = func
        self.kwargs = kwargs
        self.sleep  = sleep
        self.name   = thrname or kwargs.get("name", name(func))
        self.target = time.time() + self.sleep
        self.timer  = None

    def run(self):
        "run timer."
        self.timer.latest = time.time()
        self.func(*self.args)

    def start(self):
        "start timer."
        self.kwargs["name"] = self.name
        timer = Timy(self.sleep, self.run, *self.args, **self.kwargs)
        timer.start()
        self.timer = timer

    def stop(self):
        "stop timer."
        if self.timer:
            self.timer.cancel()


class Repeater(Timed):

    "repeater"

    def run(self):
        "run the repeater."
        launch(self.start)
        super().run()


def launch(func, *args, **kwargs):
    "run function in thread."
    thread = Thread(func, *args, **kwargs)
    thread.start()
    return thread


def level(loglevel="debug"):
    "iniitalze logging."
    if loglevel != "none":
        format_short = "%(asctime)-8s %(message)-71s"
        datefmt = "%H:%M:%S"
        logging.basicConfig(datefmt=datefmt, format=format_short, force=True)
        logging.getLogger().setLevel(LEVELS.get(loglevel))


def name(obj):
    "return name for object."
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
        'Event',
        'Handler',
        'Output',
        'Repeater',
        'Thread',
        'Timed',
        'launch',
        'level',
        'name'
   )
