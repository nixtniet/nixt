# This file is placed in the Public Domain.


"handling client events"



from .display import Display, Output
from .handler import Handler


class Client(Handler, Output):

    "display with coupled handler"

    def __init__(self):
        Handler.__init__(self)
        Output.__init__(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError


class BufferedClient(Handler, Display):

    "buffered output"

    def __init__(self):
        Handler.__init__(self)
        Display.__init__(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError

    def start(self, **kwargs):
        "start output loop."
        Handler.start(self, **kwargs)
        Display.start(self, **kwargs)

    def stop(self):
        "stop output loop."
        Handler.stop(self)
        Display.stop(self)


def __dir__():
    return (
        'BufferedClient',
        'Client'
    )
