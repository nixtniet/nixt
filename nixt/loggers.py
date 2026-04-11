# This file is placed in the Public Domain.


"logging"


import logging


class Format(logging.Formatter):

    size = 3

    def format(self, record):
        record.module = record.module.upper()
        record.module = record.module[:Format.size]
        return logging.Formatter.format(self, record)


class Log:

    datefmt = "%H:%M:%S"
    format = "%(module)-3s %(message)s"

    @staticmethod
    def size(nr):
        "set text size."
        index = Log.format.find("-")+1
        newformat = Log.format[:index]
        newformat += str(nr)
        newformat += Log.format[index+1:]
        Log.format = newformat
        Format.size = nr

    @staticmethod
    def level(loglevel):
        "set log level."
        formatter = Format(Log.format, Log.datefmt)
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        logging.basicConfig(
            level=loglevel.upper(),
            handlers=[stream,],
            force=True
        )


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
        'Log'
    )
