# This file is placed in the Public Domain.


"clients"


from .engines import Engine
from .outputs import Display, Output


class Client(Engine, Display):

    def __init__(self):
        Engine.__init__(self)
        Display.__init__(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError


class Buffered(Client, Output):

    def __init__(self):
        Client.__init__(self)
        Output.__init__(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError

    def start(self, daemon=True):
        "start output loop."
        Client.start(self)
        Output.start(self, daemon=daemon)

    def stop(self):
        "stop output loop."
        Client.stop(self)
        Output.stop(self)


def __dir__():
    return (
        'Buffered',
        'Client'
    )
