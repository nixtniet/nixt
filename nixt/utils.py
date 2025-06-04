# This file is placed in the Public Domain.


"logging"


import logging
import os
import sys


from .modules import Main


def level(loglevel="debug"):
    if loglevel != "none":
        os.environ["PYTHONUNBUFFERED"] = "yoo"
        format_short = "%(message)-80s"
        datefmt = '%H:%M:%S'
        logging.basicConfig(stream=sys.stderr, datefmt=datefmt, format=format_short)
        logging.getLogger().setLevel(LEVELS.get(loglevel))



def rlog(level, txt, ignore=None):
    if ignore is None:
        ignore = []
    for ign in ignore:
        if ign in str(txt):
            return
    logging.log(LEVELS.get(level), txt)


LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'warn': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL
         }


def __dir__():
    return (
        'level',
        'rlog'
    )
