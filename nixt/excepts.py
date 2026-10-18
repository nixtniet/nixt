# This file is placed in the Public Domain.


"default exception hanlder"


import traceback


class Errors:

    bork = False
    errors = []

    def errors():
        "print errors."
        for error in Errors.errors:
            for line in error:
                print(line)
        if not Errors.errors and "v" in cfg.opts:
            print("no errors")

    @classmethod
    def format(cls, exc):
        "format an exception"
        return traceback.format_exception(type(exc), exc, exc.__traceback__)

    @classmethod
    def later(cls, exc):
        "add an exception"
        if cls.bork:
            raise exc
        excp = exc.with_traceback(exc.__traceback__)
        fmt = format(excp)
        if fmt not in cls.errors:
            cls.errors.append(fmt)
