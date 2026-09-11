# This file is placed in the Public Domain.


"usefullness"


import logging


class Format(logging.Formatter):

    "logging format."

    disable = False
    size = 3

    def format(self, record):
        "logging formatter."
        if not Format.disable:
            record.module = record.module.upper()
            record.module = record.module[:Format.size]
        return logging.Formatter.format(self, record)


class Logging:

    "logging."

    datefmt = "%H:%M:%S"
    format = "%(module)-3s %(message)s"
    formats = "%(message)s"
    
    @classmethod
    def level(cls, loglevel, systemd=False):
        "set log level."
        formatter = Format(cls.format, cls.datefmt)
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        try:
            logging.basicConfig(
                level=loglevel.upper(),
                handlers=[stream],
                force=True
            )
        except ValueError:
            pass

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
