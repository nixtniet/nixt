# This file is placed in the Public Domain.


"logging"


import logging
import os
import time


from .encoder import Json


class Format(logging.Formatter):

    def format(self, record):
        record.module = record.module.upper()
        return logging.Formatter.format(self, record)


class Log:

    datefmt = "%H:%M:%S"
    format = "%(module).3s %(message)s"

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


class NDJson:

    def __init__(self):
        self.fpa = None
        self.fpr = None
        self.index = None
        self.last = time.time()
        self.lineno = None
        self.path = ""

    def append(self, obj):
        self.fpr.seek(0)
        txt = Json.dumps(obj)
        if txt in self.fpr.read():
            return
        self.fpa.write(Json.dumps(obj))
        self.fpa.write("\n")
        self.fpa.flush()

    def configure(self, path):
        self.path = path
        self.fpa = open(self.path, "a",  encoding="utf-8")
        self.fpr = open(self.path, "r", encoding="utf-8")

    def diff(self, nr=10):
        if self.index is None:
            self.index = os.path.getsize(self.path)
        self.fpr.seek(self.index)
        for line in range(nr):
            yield self.fpr.readline()
        self.index = self.fpr.tell()

    def watch(self):
        stamp = os.stat(self.path).st_mtime
        if stamp > self.last:
            self.last = stamp
            return True
        return False


def __dir__():
    return (
        'Log',
        'NDJson'
    )
