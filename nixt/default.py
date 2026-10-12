# This file is placed in the Public Domain.


"default imports"


import os


from argparse  import SUPPRESS, ArgumentParser
from argparse  import RawDescriptionHelpFormatter as RawFormat
from html      import unescape
from inspect   import getsourcefile
from logging   import basicConfig, Formatter, Logger, LogRecord, StreamHandler
from logging   import getLogger as Log
from os        import cpu_count, listdir, sep, unlink, walk
from os.path   import expanduser
from queue     import Queue
from random    import SystemRandom as Random
from threading import Event, RLock, Thread
from time      import sleep, time
from _thread   import interrupt_main


d = os.path.dirname
e = os.path.exists
j = os.path.join


__all__ = (
    'SUPPRESS',
    'ArgumentParser',
    'Event',
    'Formatter',
    'Log',
    'LogRecord',
    'Logger',
    'Queue',
    'RLock',
    'Random',
    'RawFormat',
    'StreamHandler',
    'Thread',
    'basicConfig',
    'cpu_count',
    'd',
    'e',
    'expanduser',
    'getsourcefile',
    'interrupt_main',
    'j',
    'listdir',
    'sep',
    'sleep',
    'time',
    'unescape',
    'unlink',
    'walk'
)


def __dir__():
    return __all__
