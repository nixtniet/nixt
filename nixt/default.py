# This file is placed in the Public Domain.


"default imports"


import datetime
import inspect
import json
import os
import threading
import time
import _thread


from argparse  import SUPPRESS, ArgumentParser
from argparse  import RawDescriptionHelpFormatter as RawFormat
from logging   import basicConfig, Formatter, LogRecord, StreamHandler
from logging   import getLogger as Logger
from queue     import Queue
from threading import Event, RLock


def __dir__():
    return (
        'SUPRESS',
        'ArgumentParser',
        'Event'.
        'Formatter',
        'Logger',
        'LogRecord',
        'Queue',
        'RawFormat',
        'RLock',
        'StreamHandler',
        'basicConfig',
        'datetime',
        'inspect',
        'json',
        'os',
        'threading',
        'time',
        '_thread'
    )


__all__ = __dir__()
