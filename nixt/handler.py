# This file is placed in the Public Domain.


"event handler"


import logging
import os
import queue
import threading
import _thread


from .threads import Thread


class Handler:

    def __init__(self):
        self.idone = threading.Event()
        self.iqueue = queue.Queue()
        self.istopped = threading.Event()

    def handle(self, event):
        "handle event."
        raise NotImplementedError

    def poller(self):
        "polling loop."
        while not self.istopped.is_set():
            self.poll()
            event = self.iqueue.get()
            if event is None:
                self.iqueue.task_done()
                break
            event.orig = repr(self)
            try:
                self.handle(event)
                self.iqueue.task_done()
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()
            except Exception as ex:
                logging.exception(ex)
                os._exit(1)
        self.idone.set()

    def poll(self):
        "create event and put it on the iqueue."

    def put(self, event):
        "put event on iqueue."
        self.iqueue.put(event)

    def start(self, daemon=True):
        "start polling loop."
        self.idone.clear()
        self.istopped.clear()
        Thread.launch(self.poller, daemon=daemon)

    def stop(self):
        "stop polling loop."
        self.istopped.set()
        self.iqueue.put(None)
        self.idone.wait()

    def wait(self):
        "wait for handler to finish."
        try:
            self.iqueue.join()
        except Exception:
            _thread.interrupt_main()


def __dir__():
    return (
        'Handler',
    )
