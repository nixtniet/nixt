# This file is placed in the Public Domain.


"debug"


import os
import sys


def debug(*args):
    for arg in args:
        sys.stderr.write(str(arg))
        sys.stderr.write("\n")
        sys.stderr.flush()


def nodebug():
    with open('/dev/null', 'a+', encoding="utf-8") as ses:
        os.dup2(ses.fileno(), sys.stderr.fileno())
