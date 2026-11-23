# This file is placed in the Public Domain.


"logging"


from logging.handlers import TimedRotatingFileHandler
from logging          import basicConfig, Formatter, StreamHandler
from logging          import getLogger as Log


logger = Log(__name__)


class Format(Formatter):

    "logging format"

    disable = False
    size = 3

    def format(self, record):
        "logging formatter."
        if not Format.disable:
            record.module = record.module.upper()
            record.module = record.module[:Format.size]
        return Formatter.format(self, record)


class Logging:

    "log"

    datefmt = "%H:%M:%S"
    format = "%(module)-3s %(message)s"
    formats = "%(message)s"

    @classmethod
    def configure(cls):
        "configure logging."
        from .configs import Main
        Main.level = Main.level or "warning"
        cls.size(len(Main.name))
        cls.level(Main.level)

    @classmethod
    def enable(cls, path, log):
        "enabke module logger."
        formatter = Format(Logging.format, Logging.datefmt)
        filehandler = TimedRotatingFileHandler(path, 'midnight')
        filehandler.setFormatter(formatter)
        if log.handlers:
            for handler in log.handlers:
                log.removeHandler(handler)
        log.addHandler(filehandler)
        log.propagate = False
        log.setLevel("DEBUG")

    @classmethod
    def level(cls, loglevel):
        "set log level."
        formatter = Format(cls.format, cls.datefmt)
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
    def size(cls, nrchars):
        "set text size."
        index = cls.format.find("-")+1
        newformat = cls.format[:index]
        newformat += str(nrchars)
        newformat += cls.format[index+1:]
        cls.format = newformat


def __dir__():
    return (
        'Format',
        'Log',
        'Logging'
    )
