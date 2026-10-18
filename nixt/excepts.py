# This file is placed in the Public Domain.


"default exception hanlder"


import traceback
import _thread


class Errors:

    bork = False
    errors = []

    @classmethod
    def format(cls, exc):
        "format an exception"
        return traceback.format_exception(type(exc), exc, exc.__traceback__)

    @classmethod
    def later(cls, exc):
        "add an exception"
        if cls.bork:
            raise exc
        if exc in (KeyboardInterrupt, EOFError):
            return _thread.interrupt_main()
        excp = exc.with_traceback(exc.__traceback__)
        fmt = format(excp)
        if fmt not in cls.errors:
            cls.errors.append(fmt)
