# This file is placed in the Public Domain.


"callback engine"


from .engines import Engine


class Handler(Engine):

    def after(self, event):
        "called after callback."

    def loop(self):
        "callback loop."
        while not self.stopped.is_set():
            self.poll()
            event = self.queue.get()
            if event is None:
                self.queue.task_done()
                break
            event.orig = repr(self)
            self.handle(event)
            self.after(event)
            self.queue.task_done()
        self.done.set()

    def poll(self):
        "create event and put it on the queue."


def __dir__():
    return (
        'Handler',
    )
