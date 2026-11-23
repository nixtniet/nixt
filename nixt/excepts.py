# This file is placed in the Public Domain.


"exception handling"


import traceback
import _thread


from .utility import Log


logger = Log(__name__)


class Errors:

    "error management"

    errors = []

    @classmethod
    def defer(cls, exc, *args):
        "add an exception."
        excp = exc.with_traceback(exc.__traceback__)
        if excp not in cls.errors:
            cls.errors.append(excp)
        try:
            args[0].ready()
        except (IndexError, AttributeError):
            pass

    @classmethod
    def format(cls, exc):
        "format an exception."
        return traceback.format_exception(type(exc), exc, exc.__traceback__)

    @classmethod
    def throw(cls, exc):
        "log the exception and interrupt main loop."
        logger.exception(exc)
        _thread.interrupt_main()


def __dir__():
    return (
        'Errors',
    )
