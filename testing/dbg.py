# This file is placed in the Public Domain.


"debug"


class Test(Exception):

    pass

def dbg(event):
    raise Test("yo!")
