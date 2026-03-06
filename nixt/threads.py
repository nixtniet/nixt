# This file is placed in the Public Domain.


"make it non-blocking"


import inspect
import logging
import os
import queue
import random
import threading
import time
import _thread


class Pool:

    def __init__(self):
        self.lock = threading.RLock()
        self.last = 0
        self.later = queue.Queue()
        self.nrcpu = 2
        self.workers = []

    def add(self, worker):
        "add worker."
        self.workers.append(worker)

    def init(self, nr=0):
        "initialisse worker pool."
        with self.lock:
            self.nrcpu = nr or self.nrcpu
            for _x in range(self.nrcpu):
                self.new()

    def new(self):
        "create new worker."
        wrk = Worker()
        wrk.start()
        self.add(wrk)
        return wrk

    def put(self, func, *args):
        if self.last >= self.nrcpu-1:
            self.last = 0
        self.workers[self.last].put(func, *args)
        self.last += 1

    def work(self, func, *args, **kwargs):
        "run function in a thread."
        if not self.workers:
            self.init()
        self.put(func, *args)


class Worker(threading.Thread):

    nr = 0

    def __init__(self, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, *args, daemon=True)
        self.event = None
        self.name = kwargs.get("name", f"Worker{Worker.nr}")
        self.once = kwargs.get("once", False)
        self.queue = queue.Queue()
        self.result = None
        self.starttime = time.time()
        self.status = "ready"
        self.stopped = threading.Event()
        Worker.nr += 1

    def __iter__(self):
        return self

    def __next__(self):
        yield from dir(self)
 
    def put(self, func, *args):
        "put function on queue."
        self.queue.put((func, args))

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
        bork = exit = False
        while 1:
            exit = False             
            func, args = self.queue.get()
            self.name = Thread.name(func)
            if args and hasattr(args[0], "ready"):
                self.event = args[0]
            try:
                self.starttime = time.time()
                self.status = "run"
                self.result = func(*args)
                self.status = "idle"
                if self.once:
                    exit = True
                    break
            except (KeyboardInterrupt, EOFError):
                exit = True
            except Exception as ex:
                logging.exception(ex)
                bork = True
            if exit or bork:
                if self.event:
                    self.event.ready()
                break
        if bork:
            _thread.interupt_main() 


class Thread:

    lock = threading.RLock()
    pool = Pool()
    
    @staticmethod
    def launch(func, *args, **kwargs):
        "run function in a thread."
        with Thread.lock:
            try:
                kwargs["once"] = True
                wrk = Worker(*args, **kwargs)
                wrk.start()
                wrk.put(func, *args)
                return wrk
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
        "push work to the workers."
        Thread.pool.put(func, *args, **kwargs)


def __dir__():
    return (
        'Pool',
        'Task',
        'Thread',
        'Worker'
    )
