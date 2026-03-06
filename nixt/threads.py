# This file is placed in the Public Domain.


"make it non-blocking"


import inspect
import logging
import os
import queue
import threading
import time
import _thread


class Task(threading.Thread):

    def __init__(self, func, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, None, (), daemon=daemon)
        self.event = None
        self.name = kwargs.get("name", Thread.name(func))
        self.queue = queue.Queue()
        self.result = None
        self.starttime = time.time()
        self.status = "init"
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
        except (KeyboardInterrupt, EOFError) as ex:
            if self.event and self.event.ready:
                self.event.ready()
            raise ex

    def run(self):
        "run function."
        func, args = self.queue.get()
        if args and hasattr(args[0], "ready"):
            self.event = args[0]
        try:
            self.status = "run"
            self.result = func(*args)
            self.status = "idle"
        except (KeyboardInterrupt, EOFError):
            if self.event:
                self.event.ready()
            _thread.interrupt_main()
        except Exception as ex:
            if self.event:
                self.event.ready()
            logging.exception(ex)
            _thread.interrupt_main()


class Worker(threading.Thread):

    nr = 0

    def __init__(self, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, *args, daemon=True, **kwargs)
        self.event = None
        self.name = kwargs.get("name", f"Worker({Worker.nr})")
        self.queue = queue.Queue()
        self.result = None
        self.starttime = time.time()
        self.status = "init"
        self.stopped = threading.Event()
        Worker.nr += 1

    def put(self, func, args):
        "put function on queue."
        self.queue.put((func, args))

    def run(self):
        "run function."
        while 1:
            func, args = self.queue.get()
            if args and hasattr(args[0], "ready"):
                self.event = args[0]
            try:
                self.status = "run"
                self.result = func(*args)
                self.status = "idle"
            except (KeyboardInterrupt, EOFError):
                if self.event:
                    self.event.ready()
                _thread.interrupt_main()
            except Exception as ex:
                if self.event:
                    self.event.ready()
                logging.exception(ex)
                _thread.interrupt_main()


class Pool:

    workers = []
    lock = threading.RLock()
    nrcpu = os.cpu_count()
    nrlast = 1

    @staticmethod
    def add(worker):
        Pool.workers.append(worker)

    @staticmethod
    def init(nrcpu=None):
        Pool.nrcpu = nrcpu or Pool.nrcpu
        for _x in range(Pool.nrcpu):
            clt = Worker()
            clt.start()
            Pool.add(clt)

    @staticmethod
    def put(func, args):
        if not Pool.workers:
            Pool.init()
        if Pool.nrlast >= Pool.nrcpu-1:
            Pool.nrlast = 0
        clt = Pool.workers[Pool.nrlast]
        clt.put(func, args)
        Pool.nrlast += 1


class Thread:

    lock = threading.RLock()

    @staticmethod
    def launch(func, *args, **kwargs):
        "run function in a thread."
        with Thread.lock:
            try:
                task = Task(func, *args, **kwargs)
                task.start()
                return task
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    @staticmethod
    def name(obj):
        "string of function/method."
        if inspect.ismethod(obj):
            return f"{obj.__self__.__class__.__name__}.{obj.__name__}"
        if inspect.isfunction(obj):
            return repr(obj).split()[1]
        return repr(obj)

    @staticmethod
    def work(func, *args, **kwargs):
        "run function in a thread."
        Pool.put(func, args)

def __dir__():
    return (
        'Repeater',
        'Thread',
        'Timed'
    )
