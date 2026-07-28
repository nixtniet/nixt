# This file is placed in the Public Domain.


"clients"


from .engines import Engine
from .outputs import Buffer, Output


class Buffered(Engine, Buffer):

    def __init__(self):
        Engine.__init__(self)
        Buffer.__init__(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError

    def start(self, daemon=True):
        "start output loop."
        Engine.start(self)
        Buffer.start(self, daemon=daemon)

    def stop(self):
        "stop output loop."
        Engine.stop(self)
        Buffer.stop(self)


class Client(Engine, Output):

    def __init__(self):
        Engine.__init__(self)
        Output.__init__(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError


def __dir__():
    return (
        'Buffered',
        'Client',
    )
