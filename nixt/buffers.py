# This file is placed in the Public Domain.


"buffered output"


import _thread


from .default import Event, Queue
from .display import Display
from .handler import Handler
from .tasking import Task


class Output(Display):

    "dedicated output loop"

    def __init__(self):
        Display.__init__(self)
        self.oqueue = Queue()
        self.ostopped = Event()

    def display(self, msg):
        "do actual display."

    def output(self):
        "output loop."
        while not self.ostopped.is_set():
            try:
                msg = self.oqueue.get()
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()
            if msg is None:
                self.oqueue.task_done()
                break
            self.display(msg)
            self.oqueue.task_done()

    def raw(self, text):
        "raw output."
        raise NotImplementedError

    def start(self, daemon=True):
        "start output loop."
        self.ostopped.clear()
        Task.start(self.output, daemon=daemon)

    def stop(self):
        "stop output loop."
        self.ostopped.set()
        self.oqueue.put(None)

    def wait(self):
        "wait for output to finish."
        try:
            self.oqueue.join()
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


class Buffer(Handler, Output):

    "buffered output"

    def __init__(self):
        Handler.__init__(self)
        Output.__init__(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError

    def start(self, daemon=True):
        "start output loop."
        Handler.start(self)
        Output.start(self, daemon=daemon)

    def stop(self):
        "stop output loop."
        Handler.stop(self)
        Output.stop(self)


def __dir__():
    return (
        'Buffer',
        'Output'
    )
