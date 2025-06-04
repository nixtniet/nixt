# This file is placed in the Public Domain.


"logging"


import logging


from .modules import Main


def init():
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger().setLevel(LEVELS.get(Main.loglevel or "debug"))



LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'warn': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL
         }
