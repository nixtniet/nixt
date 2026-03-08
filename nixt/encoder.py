# This file is placed in the Public Domain.


"encoder/decoder"


import json
import os
import types
import time


class Encoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, list):
            return iter(o)
        if isinstance(o, types.MappingProxyType):
            return dict(o)
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            try:
                return vars(o)
            except TypeError:
                return repr(o)


class Json:

    @staticmethod
    def dump(*args, **kw):
        "dump object to disk."
        kw["cls"] = Encoder
        return json.dump(*args, **kw)

    @staticmethod
    def dumps(*args, **kw):
        "dump object to string."
        kw["cls"] = Encoder
        return json.dumps(*args, **kw)

    @staticmethod
    def load(s, *args, **kw):
        "load object from disk."
        return json.load(s, *args, **kw)

    @staticmethod
    def loads(s, *args, **kw):
        "load object from string."
        return json.loads(s, *args, **kw)


class NdJson:

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
        for text in self.fpr.readlines():
            if text.find(txt) != -1:
                return
        self.fpa.write(Json.dumps(obj))
        self.fpa.write("\n")
        self.fpa.flush()
   
    def configure(self, path):
        self.path = path
        self.fpa = open(self.path, "a",  encoding="utf-8")
        self.fpr = open(self.path, "r", encoding="utf-8")

    def diff(self):
        if self.index is None:
            self.index = os.path.getsize(self.path)
        self.fpr.seek(self.index)
        yield from self.fpr.readlines()
        self.index = self.fpr.tell()

    def watch(self):
        stamp = os.stat(self.path).st_mtime
        if stamp > self.last:
            self.last = stamp
            return True
        return False


def __dir__():
    return (
        'Json',
        'NdJson'
    )
