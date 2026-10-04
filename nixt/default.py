# This file is placed in the Public Domain.


"default imports"


from argparse  import SUPPRESS, ArgumentParser
from argparse  import RawDescriptionHelpFormatter as RawFormat
from logging   import basicConfig, Formatter, LogRecord, StreamHandler
from logging   import getLogger as Logger
from queue     import Queue
from random    import SystemRandom
from threading import Event, RLock
from _thread   import LockType, allocate_lock


def __dir__():
    return (
        'SUPPRESS',
        'ArgumentParser',
        'Event',
        'Formatter',
        'LockType',
        'Logger',
        'LogRecord',
        'Queue',
        'RawFormat',
        'RLock',
        'StreamHandler',
        'SystemRandom',
        'allocate_lock',
        'basicConfig'
    )


__all__ = __dir__()
