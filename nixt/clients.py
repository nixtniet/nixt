# This file is placed in the Public Domain.


"handling client events"


import _thread


from .brokers import Broker
from .generic import Event, Queue, RLock
from .handler import Handler
from .tasking import Task


class Display:

    "unit of display"

    block = Event()
    last = ""

    def __init__(self):
        self.olock = RLock()
        self.silent = False
        Broker.add(self)

    def announce(self, text):
        "announce text to all channels."
        if not self.silent:
            self.raw(text)

    def display(self, msg):
        "display msg results."
        with self.olock:
            for txt in msg.result:
                if self.block.is_set():
                    return
                self.dosay(msg.channel, txt)
                del txt
        del msg

    def dosay(self, channel, text):
        "say called by display."
        self.say(channel, text)

    def raw(self, text):
        "raw output."
        raise NotImplementedError

    def say(self, channel, text):
        "say text in channel."
        self.last = channel
        self.raw(text)


class Output(Display):

    "dedicated output loop"

    def __init__(self):
        super().__init__()
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

    def start(self, **kwargs):
        "start output loop."
        self.ostopped.clear()
        Task.start(self.output, **kwargs)

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


class Client(Handler, Display):

    "display with coupled handler"

    def __init__(self):
        Handler.__init__(self)
        Display.__init__(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError


class Buffer(Handler, Output):

    "buffered output"

    def __init__(self):
        Handler.__init__(self)
        Output.__init__(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError

    def start(self, **kwargs):
        "start output loop."
        Handler.start(self, **kwargs)
        Output.start(self, **kwargs)

    def stop(self):
        "stop output loop."
        Handler.stop(self)
        Output.stop(self)


def __dir__():
    return (
        'Buffer',
        'Client',
        'Display',
        'Output'
    )
