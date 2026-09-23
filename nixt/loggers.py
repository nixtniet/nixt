# This file is placed in the Public Domain.


"loggers"


import logging


from logging import basicConfig, Formatter, LogRecord, StreamHandler


class Format(Formatter):

    "logging format."

    disable = False
    size = 3

    def format(self, record: LogRecord) -> str:
        "logging formatter."
        if not Format.disable:
            record.module = record.module.upper()
            record.module = record.module[:Format.size]
        return Formatter.format(self, record)


class Logging:

    "logging."

    datefmt = "%H:%M:%S"
    format = "%(module)-3s %(message)s"
    formats = "%(message)s"

    @classmethod
    def level(cls, loglevel: str) -> None:
        "set log level."
        formatter = Format(cls.formats, cls.datefmt)
        stream = StreamHandler()
        stream.setFormatter(formatter)
        try:
            basicConfig(
                level=loglevel.upper(),
                handlers=[stream],
                force=True
            )
        except ValueError:
            pass

    @classmethod
    def size(cls, nrchars: int) -> None:
        "set text size."
        index = cls.format.find("-")+1
        newformat = cls.format[:index]
        newformat += str(nrchars)
        newformat += cls.format[index+1:]
        cls.format = newformat


def __dir__():
    return (
        'Format',
        'Logging'
    )
