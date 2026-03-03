# This file is placed in the Public Domain.


"debug"


class MyException(Exception):

    pass


def dbg(event):
    raise MyException("yo!")
