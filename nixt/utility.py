# This file is placed in the Public Domain.


"usefulness"


import inspect
import logging
import os
import pathlib


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


class Utils:

    @classmethod
    def cdir(cls, path):
        "create directory."
        if os.path.exists(path):
            return
        pth = pathlib.Path(path)
        if not os.path.exists(pth.parent):
            pth.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def clsname(obj):
        "return classname of an object."
        return obj.__class__.__name__

    @staticmethod
    def home(name):
        "return home working directory."
        return os.path.expanduser(f"~/.{name}")

    @staticmethod
    def listdir(path, ignore=""):
        "list modules in a directory."
        return [
                x[:-3] for x in os.listdir(path)
                if x.endswith(".py") and
                not x.startswith("__") and
                x[:-3] not in Utils.spl(ignore)
               ]

    @staticmethod
    def skip(obj):
        "skip underscored keys."
        result = []
        for x in dir(obj):
            if x.startswith("_"):
                continue
            result.append(x)
        return sorted(result)

    @staticmethod
    def skipped(obj):
        "yield values without underscored keys."
        for key in dir(obj):
            if key.startswith("_"):
                continue
            yield getattr(obj, key)

    @staticmethod
    def source(module):
        "return the source of a module."
        return module.__loader__.get_source(module.__name__)

    @staticmethod
    def spl(txt, ignore=""):
        "list from comma seperated string."
        try:
            ignores = ignore.split(",")
            result = txt.split(",")
        except (TypeError, ValueError):
            result = []
        return [x for x in result if x and x not in ignores]

    @staticmethod
    def strip(path, nr=3):
        "strip filename from path."
        return os.path.join(*path.split(os.sep)[-nr:])

    @staticmethod
    def where(obj):
        "path where object is defined."
        return os.path.dirname(inspect.getfile(obj))


def __dir__():
    return (
        'Format',
        'Logging'
        'Utils'
    )
