# This file is placed in the Public Domain.


"handling client events"


import _thread


from .tasking import Tasks
from .utility import Event, Queue, RLock


class Display:

    "unit of display"

    block = Event()
    last = ""

    def __init__(self):
        self.olock = RLock()
        self.silent = False

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
            msg.ready()
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
        Tasks.start(self.output, **kwargs)

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


def __dir__():
    return (
        'Display',
        'Output'
    )
