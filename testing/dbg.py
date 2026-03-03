# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"debug"


class MyException(Exception):

    pass


def dbg(event):
    raise MyException("yo!")
