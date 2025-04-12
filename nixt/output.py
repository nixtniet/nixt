# This file is placed in the Public Domain.


"output"


import sys


def doprint(txt):
    print(txt.rstrip())
    sys.stdout.flush()


def output(txt):
    doprint(txt)


def nil(txt):
    pass


def enable():
    global output
    output = doprint


def disable():
    global output
    output = nil


def __dir__():
    return (
        'disable',
        'enable',
        'output'
    )
