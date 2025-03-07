# This file is placed in the Public Domain.


"deferred exception handling"


import os
import sys
import traceback




class Errors:

    name = __file__.rsplit("/", maxsplit=2)[-2]
    errors = []

    @staticmethod
    def format(exc) -> str:
        exctype, excvalue, trb = type(exc), exc, exc.__traceback__
        trace = traceback.extract_tb(trb)
        result = ""
        for i in trace:
            fname = i[0]
            if fname.endswith(".py"):
                fname = fname[:-3]
            linenr = i[1]
            plugfile = fname.split("/")
            mod = []
            for i in plugfile[::-1]:
                mod.append(i)
                if Errors.name in i or "bin" in i:
                    break
            ownname = '.'.join(mod[::-1])
            if ownname.endswith("__"):
                continue
            if ownname.startswith("<"):
                continue
            result += f"{ownname}:{linenr} "
        del trace
        res = f"{exctype} {result[:-1]} {excvalue}"
        return res

    @staticmethod
    def full(exc) -> str:
        return traceback.format_exception(
            type(exc),
            exc,
            exc.__traceback__
        )


def debug(*args):
    for arg in args:
        sys.stderr.write(str(arg))
        sys.stderr.write("\n")
        sys.stderr.flush()


def later(exc) -> None:
    excp = exc.with_traceback(exc.__traceback__)
    fmt = Errors.format(excp)
    if fmt not in Errors.errors:
        Errors.errors.append(fmt)


def nodebug():
    with open('/dev/null', 'a+', encoding="utf-8") as ses:
        os.dup2(ses.fileno(), sys.stderr.fileno())


def __dir__():
    return (
        'Errors',
        'debug',
        'later',
        'nodebug'
    )
