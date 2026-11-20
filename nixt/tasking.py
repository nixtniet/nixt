# This file is placed in the Public Domain.


"non-blocking"


import time


from .excepts import Errors
from .generic import Event, Queue, RLock, Thread
from .loggers import Log
from .methods import Methods


logger = Log(__name__)


class Work(Thread):

    "unit of work"

    block = Event()
    lock = RLock()

    def __init__(self, func, *args, **kwargs):
        super().__init__(
            None,
            self.run,
            None,
            (),
            daemon=kwargs.get("daemon",True)
        )
        self.name = kwargs.get("name", Methods.getname(func))
        self.queue = Queue()
        self.result = None
        self.sleep = 0.0
        self.starttime = time.time()
        self.state = {}
        self.queue.put((func, args))

    def __iter__(self):
        return self

    def __next__(self):
        yield from dir(self)

    def join(self, timeout=None):
        "join thread and return result."
        try:
            super().join(timeout or None)
            return self.result
        except Exception as ex:
            self.block.set()
            Errors.throw(ex)

    def run(self):
        "run function."
        func, args = self.queue.get()
        if self.block.is_set():
            return
        try:
            self.result = func(*args)
        except Exception as ex:
            self.block.set()
            Errors.throw(ex)


class Task:

    "start a task"

    lock = RLock()

    @classmethod
    def start(cls, func, *args, **kwargs):
        "start a new thread running function with arguments."
        with cls.lock:
            work = Work(func, *args, **kwargs)
            work.start()
            return work


def __dir__():
    return (
        'Task',
        'Work'
    )
