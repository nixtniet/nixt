# This file is placed in the Public Domain.


"logging"


import logging.handlers


from .default import basicConfig, Formatter, Logger, LogRecord, StreamHandler
from .typings import ClassVar


class Format(Formatter):

    "logging format"

    disable: ClassVar[bool] = False
    size: ClassVar[int] = 3

    def format(self, record: LogRecord) -> str:
        "logging formatter."
        if not Format.disable:
            record.module = record.module.upper()
            record.module = record.module[:Format.size]
        return Formatter.format(self, record)


class Logging:

    "log"

    datefmt: ClassVar[str] = "%H:%M:%S"
    format:  ClassVar[str] = "%(module)-3s %(message)s"
    formats: ClassVar[str] = "%(message)s"

    @classmethod
    def enable(cls, path: str, logger: Logger) -> None:
        "enabke module logger."
        formatter = Format(Logging.formats, Logging.datefmt)
        filehandler = logging.handlers.TimedRotatingFileHandler(path, 'midnight')
        filehandler.setFormatter(formatter)
        if logger.handlers:
            for handler in logger.handlers:
                logger.removeHandler(handler)
        logger.addHandler(filehandler)
        logger.propagate = False
        logger.setLevel("DEBUG")

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
