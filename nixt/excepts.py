# This file is placed in the Public Domain.


"default exception handler"


import os
import traceback
import _thread


from .default import Log
from .message import Message


logger = Log(__name__)


class Errors:

    "error management"

    errors = []

    @classmethod
    def format(cls, exc):
        "format an exception"
        return traceback.format_exception(type(exc), exc, exc.__traceback__)

    @classmethod
    def defer(cls, exc, *args):
        "add an exception"
        excp = exc.with_traceback(exc.__traceback__)
        if excp not in cls.errors:
            cls.errors.append(excp)
        if args and isinstance(args[0], Message):
            args[0].ready()

    @classmethod
    def line(cls, exc, *args):
        res = []
        fmt = cls.format(exc, *args)
        for line in fmt[::-1]:
            spl = line.split()
            if not spl:
                continue
            if spl[0] != "File":
                continue
            filename = spl[1].split(os.sep)[-1][:-5]
            lineno = spl[3]
            res.append(f"{filename}:{lineno}")
        res.append(fmt[-1])
        return " | ".join(res)

    @classmethod
    def throw(cls, exc, *args):
        "log the exception and interrupt main loop."
        logger.exception(exc)
        _thread.interrupt_main()


def __dir__():
    return (
        'Errors',
    )
