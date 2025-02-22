# This file is placed in the Public Domain.


"buffers"


import queue
import threading


from .thread  import launch


class Output:

    def __init__(self):
        self.oqueue   = queue.Queue()
        self.running = threading.Event()

    def loop(self) -> None:
        self.running.set()
        while self.running.is_set():
            evt = self.oqueue.get()
            if evt is None:
                self.oqueue.task_done()
                break
            evt.display()
            self.oqueue.task_done()

    def oput(self,evt) -> None:
        self.oqueue.put(evt)

    def start(self) -> None:
        if not self.running.is_set():
            self.running.set()
            launch(self.loop)

    def stop(self) -> None:
        self.running.clear()
        self.oqueue.put(None)

    def wait(self) -> None:
        self.oqueue.join()
        self.running.wait()


def __dir__():
    return (
        'Output',
    )
