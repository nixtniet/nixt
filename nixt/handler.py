# This file is placed in the Public Domain.


"message handler"


import os
import _thread


from .objects import Methods
from .threads import Threads
from .utility import Event, Queue, RLock


class Handler:

    "keep looping"

    def __init__(self):
        self.queue = Queue()
        self.running = Event()
        self.done = Event()

    def after(self, msg):
        "called after callback."

    def handle(self, msg):
        "override this."

    def loop(self):
        "callback loop."
        while self.running.is_set():
            self.poll()
            msg = self.queue.get()
            if msg is None:
                self.queue.task_done()
                break
            msg.orig = repr(self)
            self.handle(msg)
            self.after(msg)
            self.queue.task_done()
        self.done.set()

    def poll(self):
        "create msg and put it on the queue."

    def put(self, msg):
        "put msg on queue."
        self.queue.put(msg)

    def start(self, **kwargs):
        "start callback loop."
        self.done.clear()
        self.running.set()
        Threads.start(self.loop, **kwargs)

    def stop(self):
        "stop xallback loop."
        if not self.running.is_set():
            return
        self.running.clear()
        self.queue.put(None)
        self.done.wait()

    def wait(self):
        "wait for all msgs to finish."
        try:
            self.queue.join()
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


class Engine(Handler):

    "callback engine"

    def __init__(self):
        super().__init__()
        self.cbs = {}

    def handle(self, msg):
        "run callback function with msg."
        func = self.cbs.get(msg.kind, None)
        if not func:
            msg.ready()
            return
        name = msg.text and msg.text.split()[0]
        msg.thread(Threads.start(func, msg, name=name))

    def register(self, kind, callback):
        "register callback."
        self.cbs[kind] = callback


class Runner(Handler):

    "run jobs"

    def run(self, *args, **kwargs):
        "running."

    def loop(self):
        "loop to handle fetch jobs."
        while self.running.is_set():
            job = self.queue.get()
            if job is None:
                break
            self.run(*job)
        self.done.set()

    def wait(self):
        "skip wait."


class Pool:

    "multiple runners"

    runners = []
    lock = RLock()
    max = os.cpu_count()
    nrcpu = 1
    nrlast = 0

    @classmethod
    def add(cls, runner):
        "add a runner."
        cls.runners.append(runner)

    @classmethod
    def busy(cls):
        "see if pool is busy."
        return any(runner.queue.qsize() for runner in cls.runners)

    @classmethod
    def init(cls, nrs, clz):
        "initialze a number of runners."
        cls.nrcpu = nrs
        for nr in range(nrs):
            runner = clz()
            runner.start(name=f"{Methods.clsname(runner)}{nr}")
            cls.add(runner)

    @classmethod
    def put(cls, *args):
        "push job to a runner."
        with cls.lock:
            if cls.nrlast-1 >= len(cls.runners)-1:
                cls.nrlast = 0
            clt = cls.runners[cls.nrlast-1]
            clt.put(*args)
            cls.nrlast += 1


def __dir__():
    return (
        'Engine',
        'Handler',
        'Message',
        'Pool',
        'Runner'
    )
