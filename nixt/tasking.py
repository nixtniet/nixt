# This file is placed in the Public Domain.


"non-blocking"


import time


from .excepts import Errors
from .methods import Methods
from .utility import Event, Log, Queue, RLock, Thread


logger = Log(__name__)


class Task(Thread):

    "unit of thread"

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

    @classmethod
    def begin(cls, func, *args, **kwargs):
        "start a new thread running function with arguments."
        with cls.lock:
            task = Task(func, *args, **kwargs)
            task.start()
            return task

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


def __dir__():
    return (
        'Task',
    )
