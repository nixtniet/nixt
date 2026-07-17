# This file is placed in the Public Domain.


"callback engine"


import inspect
import logging
import queue
import threading
import time
import _thread


from .objects import Object


class Engine:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        self.done = threading.Event()

    def after(self, event):
        "called after callback."

    def callback(self, event):
        "run callback function with event."
        func = self.cbs.get(event.kind, None)
        if not func:
            event.ready()
            return
        name = event.text and event.text.split()[0]
        event._thr = Thread.launch(func, event, name=name)

    def loop(self):
        "callback loop."
        while not self.stopped.is_set():
            self.poll()
            event = self.queue.get()
            if event is None:
                self.queue.task_done()
                break
            event.orig = repr(self)
            self.callback(event)
            self.after(event)
            self.queue.task_done()
        self.done.set()

    def poll(self):
        "create event and put it on the queue."

    def put(self, event):
        "put event on queue."
        self.queue.put(event)

    def register(self, kind, callback):
        "register callback."
        self.cbs[kind] = callback

    def start(self, daemon=True):
        "start callback loop."
        self.done.clear()
        self.stopped.clear()
        Thread.launch(self.loop, daemon=daemon)

    def stop(self):
        "stop xallback loop."
        self.stopped.set()
        self.queue.put(None)
        self.done.wait()

    def wait(self):
        "wait for all events to finish,"
        try:
            self.queue.join()
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


class Repeater:

    counter = 0
    running = threading.Event()
    stopped = threading.Event()
    todo = Object()

    @classmethod
    def add(cls, sleep, func, *args, **kwargs):
        "add a repeater."
        if not cls.running.is_set():
            cls.start()
        sleep = str(sleep)
        if sleep not in cls.todo:
            cls.todo[sleep] = []
        cls.todo[sleep].append((func, args, kwargs))

    @classmethod
    def loop(cls):
        "repeater loop."
        while not cls.stopped.is_set():
            time.sleep(1.0)
            cls.counter += 1
            for sleep in cls.todo:
                slept = float(sleep)
                if cls.counter % slept != 0:
                    continue
                for func, args, kwargs in cls.todo[sleep]:
                    Thread.launch(func, *args, **kwargs)

    @classmethod
    def start(cls):
        "start repeater loop."
        cls.running.set()
        cls.stopped.clear()
        Thread.launch(cls.loop, name="Repeater.loop")

    @classmethod
    def stop(cls):
        "stop repeater loop."
        cls.stopped.set()


class Task(threading.Thread):

    block = threading.Event()

    def __init__(self, func, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, None, (), daemon=daemon)
        self.event = None
        self.name = kwargs.get("name", Thread.name(func))
        self.queue = queue.Queue()
        self.result = None
        self.starttime = time.time()
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
            _thread.interrupt_main()

    def run(self):
        "run function."
        func, args = self.queue.get()
        if self.block.is_set():
            return
        try:
            self.result = func(*args)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


class Thread:

    lock = threading.RLock()

    @classmethod
    def launch(cls, func, *args, **kwargs):
        "start a new thread running function with arguments."
        with cls.lock:
            "run function in a thread."
            task = Task(func, *args, **kwargs)
            task.start()
            return task

    @classmethod
    def clsname(cls, obj):
        "class name of an object."
        if "__self__" in dir(obj):
            return obj.__self__.__class__.__name__
        return obj.__class__.__name_

    @classmethod
    def name(cls, obj):
        "string of function/method."
        if inspect.ismethod(obj):
            return f"{cls.clsname(obj)}.{obj.__name__}"
        if inspect.isfunction(obj):
            return repr(obj).split()[1]
        return repr(obj)


def __dir__():
    return (
        'Engine',
        'Repeater',
        'Task',
        'Thread'
    )
