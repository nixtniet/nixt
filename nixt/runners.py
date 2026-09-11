# This file is placed in the Public Domain.


"the big loop"


from .looping import Loop
from .threads import Thread


class Runner(Loop):

    "run job."

    def run(self, *args, **kwargs):
        "fetch a feed."
        raise NotImplementedError

    def loop(self):
        "loop to handle fetch jobs."
        while not self.stopped.is_set():
            job = self.queue.get()
            if job is None:
                break
            self.run(*job)

    def start(self, daemon=True):
        "start callback loop."
        self.done.clear()
        self.stopped.clear()
        Thread.launch(self.loop, daemon=daemon, name="Runner.loop")


def __dir__():
    return (
        'Runner',
    )
