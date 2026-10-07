# This file is placed in the Public Domain.


"buffered output"


from .handler import Handler
from .outputs import Output


class Buffer(Handler, Output):

    "buffered output"

    def __init__(self):
        Handler.__init__(self)
        Output.__init__(self)

    def raw(self, text: str) -> None:
        "raw output."
        raise NotImplementedError

    def start(self, daemon: bool = True) -> None:
        "start output loop."
        Handler.start(self)
        Output.start(self, daemon=daemon)

    def stop(self) -> None:
        "stop output loop."
        Handler.stop(self)
        Output.stop(self)


def __dir__():
    return (
        'Buffer',
    )
