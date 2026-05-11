# This file is placed in the Public Domain.


"logging"


import logging


class Format(logging.Formatter):

    disable = False
    size = 4

    def format(self, record):
        "logging formatter."
        if not Format.disable:
            record.module = record.module.upper()
            record.module = record.module[:Format.size]
        return logging.Formatter.format(self, record)


class Log:

    datefmt = "%H:%M:%S"
    format = "%(module)-3s %(message)s"

    @classmethod
    def level(cls, loglevel):
        "set log level."
        formatter = Format(Log.format, Log.datefmt)
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        logging.basicConfig(
            level=loglevel.upper(),
            handlers=[stream,],
            force=True
        )

    @classmethod
    def size(cls, nr):
        "set text size."
        index = cls.format.find("-")+1
        newformat = cls.format[:index]
        newformat += str(nr)
        newformat += cls.format[index+1:]
        cls.format = newformat


LEVELS = {
    "notset": logging.NOTSET,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
    "fatal": logging.FATAL
}

def __dir__():
    return (
        'LEVELS',
        'Format',
        'Log'
    )
