# This file is placed in the Public Domain.


"the big loop"


import _thread


from .default import Event, Queue
from .dqueues import DQueue
from .message import Message
from .persist import Workdir
from .tasking import Task
from .typings import Union


class Loop:

    "keep looping"

    def __init__(self):
        self.queue: Queue = DQueue(Workdir.runpath("loop"))
        # self.queue = Queue()
        self.stopped: Event = Event()
        self.done: Event = Event()

    def after(self, msg: Message) -> None:
        "called after callback."

    def handle(self, msg: Message) -> None:
        "handle msg."

    def loop(self) -> None:
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

    def poll(self) -> Union[Message, None]:
        "create msg and put it on the queue."

    def put(self, msg: Message) -> None:
        "put msg on queue."
        self.queue.put(msg)

    def start(self, daemon: bool = True) -> None:
        "start callback loop."
        self.done.clear()
        self.stopped.clear()
        Task.start(self.loop, daemon=daemon)

    def stop(self) -> None:
        "stop xallback loop."
        self.stopped.set()
        self.queue.put(None)
        self.done.wait()

    def wait(self) -> None:
        "wait for all msgs to finish,"
        try:
            self.queue.join()
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def __dir__():
    return (
        'Loop',
    )
