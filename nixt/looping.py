# This file is placed in the Public Domain.


"the big loop"


import queue
import threading
import _thread


from queue  import Queue
from typing import Union


from .message import Message
from .threads import Thread


class Loop:

    "keep looping"

    def __init__(self):
        self.queue: Queue = queue.Queue()
        self.stopped = threading.Event()
        self.done = threading.Event()

    def after(self, message: Message) -> None:
        "called after callback."

    def handle(self, message: Message) -> None:
        "handle message."

    def loop(self) -> None:
        "callback loop."
        while not self.stopped.is_set():
            self.poll()
            message = self.queue.get()
            if message is None:
                self.queue.task_done()
                break
            message.orig = repr(self)
            self.handle(message)
            self.after(message)
            self.queue.task_done()
        self.done.set()

    def poll(self) -> Union[Message, None]:
        "create message and put it on the queue."

    def put(self, message: Message) -> None:
        "put message on queue."
        self.queue.put(message)

    def start(self, daemon: bool = True) -> None:
        "start callback loop."
        self.done.clear()
        self.stopped.clear()
        Thread.launch(self.loop, daemon=daemon)

    def stop(self) -> None:
        "stop xallback loop."
        self.stopped.set()
        self.queue.put(None)
        self.done.wait()

    def wait(self) -> None:
        "wait for all messages to finish,"
        try:
            self.queue.join()
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def __dir__():
    return (
        'Loop',
    )
