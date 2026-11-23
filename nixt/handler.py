# This file is placed in the Public Domain.


"message handler"


import _thread


from .tasking import Tasks
from .utility import Event, Queue


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
        Tasks.start(self.loop, **kwargs)

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
        msg.thread(Tasks.start(func, msg, name=name))

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


def __dir__():
    return (
        'Engine',
        'Handler',
        'Runner'
    )
