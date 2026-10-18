# This file is placed in the Public Domain.


"default exception hanlder"


import traceback
import _thread


from .message import Message


class Errors:

    bork = False
    errors = []

    @classmethod
    def format(cls, exc):
        "format an exception"
        return traceback.format_exception(type(exc), exc, exc.__traceback__)

    @classmethod
    def defer(cls, exc, *args):
        "add an exception"
        if cls.bork:
            raise exc
        if exc in (KeyboardInterrupt, EOFError):
            return _thread.interrupt_main()
        excp = exc.with_traceback(exc.__traceback__)
        if excp not in cls.errors:
            cls.errors.append(excp)
        if args and isinstance(args[0], Message):
            args[0].ready()
    