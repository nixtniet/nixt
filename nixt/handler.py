# This file is placed in the Public Domain.


"handler"


import inspect
import logging
import queue
import threading
import time
import _thread

from .command import Commands


class Handler:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()
        self.running = threading.Event()

    def callback(self, event):
        "run callback function with event."
        func = self.cbs.get(event.kind, None)
        if not func:
            event.ready()
            return
        name = event.text and event.text.split()[0]
        event._thr = Thread.launch(func, event, name=name)

    def loop(self):
        "event loop."
        while self.running.is_set():
            event = self.queue.get()
            if not event:
                break
            event.orig = repr(self)
            self.callback(event)

    def put(self, event):
        "put event on queue."
        self.queue.put(event)

    def register(self, kind, callback):
        "register callback."
        self.cbs[kind] = callback

    def start(self):
        "start event handler loop."
        self.running.set()
        Thread.launch(self.loop)

    def stop(self):
        "stop event handler loop."
        self.running.clear()
        self.queue.put(None)


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.iqueue = queue.Queue()
        self.olock = threading.RLock()
        self.silent = True
        self.stopped = threading.Event()

    def announce(self, text):
        "announce text to all channels."
        if not self.silent:
            self.raw(text)

    def display(self, event):
        "display event results."
        with self.olock:
            for tme in event.result:
                self.dosay(event.channel, event.result.get(tme))

    def dosay(self, channel, text):
        "say called by display."
        self.say(channel, text)

    def loop(self):
        "input loop."
        while True:
            event = self.poll()
            if not event or self.stopped.is_set():
                break
            event.orig = repr(self)
            Commands.command(event)

    def poll(self):
        "return event."
        return self.iqueue.get()

    def put(self, event):
        self.iqueue.put(event)

    def raw(self, text):
        "raw output."

    def say(self, channel, text):
        "say text in channel."
        self.raw(text)

    def start(self):
        "start handler."
        Thread.launch(self.loop)


class Task(threading.Thread):

    last = time.time()

    def __init__(self, func, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, None, (), daemon=daemon)
        self.event = None
        self.name = kwargs.get("name", Thread.name(func))
        self.queue = queue.Queue()
        self.result = None
        self.starttime = time.time()
        self.stopped = threading.Event()
        self.queue.put((func, args))

    def __iter__(self):
        return self

    def __next__(self):
        yield from dir(self)

    def join(self, timeout=0.0):
        "join thread and return result."
        try:
            super().join(timeout or None)
            return self.result
        except (KeyboardInterrupt, EOFError):
            if self.event and self.event.ready:
                self.event.ready()
            _thread.interrupt_main()

    def run(self):
        "run function."
        if time.time() - Task.last < 0.01:
            time.sleep(0.01)
        Task.last = time.time()
        func, args = self.queue.get()
        if args and hasattr(args[0], "ready"):
            self.event = args[0]
        try:
            self.result = func(*args)
            return self.result
        except (KeyboardInterrupt, EOFError):
            pass
        except Exception as ex:
            logging.exception(ex)
        if self.event:
            self.event.ready()
        _thread.interrupt_main()


class Thread:

    lock = threading.RLock()

    @classmethod
    def launch(cls, func, *args, **kwargs):
        "run function in a thread."
        with cls.lock:
            try:
                task = Task(func, *args, **kwargs)
                task.start()
                return task
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    @classmethod
    def name(cls, obj):
        "string of function/method."
        if inspect.ismethod(obj):
            return f"{obj.__func__.__qualname__}"
        if inspect.isfunction(obj):
            return repr(obj).split()[1]
        return repr(obj)


def __dir__():
    return (
        "Handler",
        "Thread"
    )
