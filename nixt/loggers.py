# This file is placed in the Public Domain.


"logging"


import logging


class Format(logging.Formatter):

    disable = False
    size = 3

    def format(self, record):
        "logging formatter."
        if not Format.disable:
            record.module = record.module.upper()
            record.module = record.module[:Format.size]
        return logging.Formatter.format(self, record)


class Logging:

    datefmt = "%H:%M:%S"
    format = "%(module)-3s %(message)s"

    @classmethod
    def level(cls, loglevel, systemd=False):
        "set log level."
        formatter = Format(cls.format, Logging.datefmt)
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


def __dir__():
    return (
        'Format',
        'Logging'
    )
