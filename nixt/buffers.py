# This file is placed in the Public Domain.


"clients"


import logging
import queue
import threading
import _thread


from .clients import Output
from .engines import Engine
from .threads import Thread


class Buffer(Output):

    def __init__(self):
        Output.__init__(self)
        self.oqueue = queue.Queue()
        self.ostopped = threading.Event()

    def output(self):
        "output loop."
        while not self.ostopped.is_set():
            try:
                event = self.oqueue.get()
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()
            if event is None:
                self.oqueue.task_done()
                break
            self.display(event)
            self.oqueue.task_done()

    def raw(self, text):
        "raw output."
        raise NotImplementedError

    def start(self, daemon=True):
        "start output loop."
        self.ostopped.clear()
        Thread.launch(self.output, daemon=daemon)

    def stop(self):
        "stop output loop."
        self.ostopped.set()
        self.oqueue.put(None)

    def wait(self):
        "wait for output to finish."
        try:
            self.oqueue.join()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


class Buffered(Engine, Buffer):

    def __init__(self):
        Engine.__init__(self)
        Buffer.__init__(self)

    def start(self):
        "start buffered client."
        Engine.start(self)
        Buffer.start(self)

    def stop(self):
        "stop buffered client."
        Engine.stop(self)
        Buffer.stop(self)


def __dir__():
    return (
        'Buffer',
        'Buffered'
    )
