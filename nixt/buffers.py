# This file is placed in the Public Domain.


"buffered output"


import _thread


from .default import Event, Queue
from .display import Display
from .engines import Engine
from .message import Message
from .threads import Threading


class Output(Display):

    "dedicated output loop"

    def __init__(self):
        Display.__init__(self)
        self.oqueue: Queue = Queue()
        self.ostopped: Event = Event()

    def display(self, msg: Message) -> None:
        "do actual display."

    def output(self) -> None:
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

    def raw(self, text: str) -> None:
        "raw output."
        raise NotImplementedError

    def start(self, daemon: bool = True) -> None:
        "start output loop."
        self.ostopped.clear()
        Threading.launch(self.output, daemon=daemon)

    def stop(self) -> None:
        "stop output loop."
        self.ostopped.set()
        self.oqueue.put(None)

    def wait(self) -> None:
        "wait for output to finish."
        try:
            self.oqueue.join()
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


class Buffer(Engine, Output):

    "buffered output"

    def __init__(self):
        Engine.__init__(self)
        Output.__init__(self)

    def raw(self, text: str) -> None:
        "raw output."
        raise NotImplementedError

    def start(self, daemon: bool = True) -> None:
        "start output loop."
        Engine.start(self)
        Output.start(self, daemon=daemon)

    def stop(self) -> None:
        "stop output loop."
        Engine.stop(self)
        Output.stop(self)


def __dir__():
    return (
        'Buffer',
        'Output'
    )
