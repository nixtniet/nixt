# This file is placed in the Public Domain.


"default imports"


from argparse  import SUPPRESS, ArgumentParser
from argparse  import RawDescriptionHelpFormatter as RawFormat
from logging   import basicConfig, Formatter, LogRecord, StreamHandler
from logging   import getLogger as Logger
from queue     import Queue
from random    import SystemRandom as Random
from threading import Event, RLock
from _thread   import LockType, allocate_lock


__all__ = (
    'SUPPRESS',
    'ArgumentParser',
    'Event',
    'Formatter',
    'LockType',
    'LogRecord',
    'Logger',
    'Queue',
    'RLock',
    'Random',
    'RawFormat',
    'StreamHandler',
    'allocate_lock',
    'basicConfig'
)


def __dir__():
    return __all__
