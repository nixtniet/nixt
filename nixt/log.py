# This file is placed in the Public Domain.


"logging"


import logging
import sys


def level(loglevel="debug"):
    if loglevel != "none":
        format_short = "%(message)-80s"
        datefmt = "%H:%M:%S"
        logging.basicConfig(stream=sys.stderr, datefmt=datefmt, format=format_short)
        logging.getLogger().setLevel(LEVELS.get(loglevel))


def rlog(loglevel, txt, ignore=None):
    if ignore is None:
        ignore = []
    for ign in ignore:
        if ign in str(txt):
            return
    logging.log(LEVELS.get(loglevel), txt)


"data"


LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "warn": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


"interface"


def __dir__():
    return (
        "level",
        "rlog"
    )
