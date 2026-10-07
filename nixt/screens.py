# This file is placed in the Public Domain.


"an object for a string"


from .display import Display
from .handler import Handler


class Screen(Handler, Display):

    "display wit coupled handler."

    def __init__(self):
        Handler.__init__(self)
        Display.__init__(self)

    def raw(self, text: str) -> None:
        "raw output."
        raise NotImplementedError


def __dir__():
    return (
        'Screen',
    )
