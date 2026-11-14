# This file is placed in the Public Domain.


"the big loop"


import _thread


from .tasking import Task
from .utility import Event, Queue


class Loop:

    "keep looping"

    def __init__(self):
        self.queue = Queue()
        self.stopped = Event()
        self.done = Event()

    def after(self, msg):
        "called after callback."

    def handle(self, msg):
        "handle msg."

    def loop(self):
        "callback loop."
        while not self.stopped.is_set():
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

    def start(self, daemon=True, name=None):
        "start callback loop."
        self.done.clear()
        self.stopped.clear()
        Task.start(self.loop, daemon=daemon, name=name)

    def stop(self):
        "stop xallback loop."
        self.stopped.set()
        self.queue.put(None)
        self.done.wait()

    def wait(self):
        "wait for all msgs to finish."
        try:
            self.queue.join()
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


class Handler(Loop):

    "run callbacks"

    def __init__(self):
        super().__init__()
        self.cbs = {}

    def handle(self, msg):
        "run callback function with msg."
        func = self.cbs.get(msg.kind, None)
        if not func:
            msg.ready()
            return
        name = msg.text.strip() and msg.text.split()[0]
        msg.thread(Task.start(func, msg, name=name))

    def register(self, kind, callback):
        "register callback."
        self.cbs[kind] = callback


class Runner(Loop):

    "run jobs"

    def run(self, *args, **kwargs):
        "fetch a feed."
        raise NotImplementedError

    def loop(self):
        "loop to handle fetch jobs."
        while not self.stopped.is_set():
            job = self.queue.get()
            if job is None:
                break
            self.run(*job)
        self.done.set()

    def wait(self):
        "skip wait."


def __dir__():
    return (
        'Handler',
        'Loop',
        'Runner'
    )
