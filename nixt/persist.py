# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,W0105,E0402


"persistence through storage"


import json
import os
import pathlib
import threading


from .encoder import dump, load
from .methods import deleted, fqn, ident, search
from .objects import Default, keys, update
from .utility import fntime


"cache"


class Cache:

    paths = {}

    def add(self, path, obj):
        "put object into cache."
        self.paths[path] = obj

    def get(self, path):
        "get object from cache."
        return self.paths.get(path, None)

    def sync(self, path, obj):
        "update cached object."
        try:
            update(self.paths[path], obj)
        except KeyError:
            self.add(path, obj)


"persist"


class Persist:

    cache = Cache()
    lock = threading.RLock()
    wdr = ""

    def attrs(self, kind):
        "show attributes for kind of objects."
        result = []
        for _pth, obj in self.find(kind):
            result.extend(keys(obj))
        return set(result)

    def count(self, kind):
        "count number of object of a certain kind."
        return len(list(self.find(kind)))

    def find(self, kind, selector=None, removed=False, matching=False):
        "locate objects by matching atributes."
        if selector is None:
            selector = {}
        for pth in self.fns(self.long(kind)):
            obj = self.cache.get(pth)
            if not obj:
                obj = Default()
                self.read(obj, pth)
            self.cache.add(pth, obj)
            if not removed and deleted(obj):
                continue
            if selector and not search(obj, selector, matching):
                continue
            yield pth, obj

    def first(self, obj, selector=None):
        "return first version of an object."
        if selector is None:
            selector = {}
        result = sorted(
                        self.find(fqn(obj), selector),
                        key=lambda x: fntime(x[0])
                       )
        res = ""
        if result:
            inp = result[0]
            update(obj, inp[-1])
            res = inp[0]
        return res

    def fns(self, kind):
        "file names by kind of object."
        path = os.path.join(self.wdr, "store", kind)
        for rootdir, dirs, _files in os.walk(path, topdown=True):
            for dname in dirs:
                if dname.count("-") != 2:
                    continue
                ddd = os.path.join(rootdir, dname)
                for fll in os.listdir(ddd):
                    yield strip(os.path.join(ddd, fll))

    def kinds(self):
        "show kind on objects in cache."
        return os.listdir(os.path.join(self.wdr, "store"))

    def last(self, obj, selector=None):
        "last saved version."
        if selector is None:
            selector = {}
        result = sorted(
                        self.find(fqn(obj), selector),
                        key=lambda x: fntime(x[0])
                      )
        res = ""
        if result:
            inp = result[-1]
            update(obj, inp[-1])
            res = inp[0]
        return res

    def long(self, name):
        "expand to fqn."
        if "." in name:
            return name
        split = name.split(".")[-1].lower()
        res = name
        for names in self.kinds():
            if split == names.split(".")[-1].lower():
                res = names
                break
        return res

    def pidfile(self, name):
        "write pidfile."
        filename = os.path.join(self.wdr, f"{name}.pid")
        if os.path.exists(filename):
            os.unlink(filename)
        path2 = pathlib.Path(filename)
        path2.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as fds:
            fds.write(str(os.getpid()))

    def read(self, obj, path, base="store"):
        "read object from path."
        with self.lock:
            pth = os.path.join(self.wdr, base, path)
            if not os.path.exists(pth):
                return
            with open(pth, "r", encoding="utf-8") as fpt:
                try:
                    update(obj, load(fpt))
                except json.decoder.JSONDecodeError as ex:
                    ex.add_note(path)
                    raise ex

    def setwd(self, path):
        "enable writing to disk."
        Persist.wdr = path
        self.skel()

    def skel(self):
        "create directories."
        if not self.wdr:
            return
        path = os.path.abspath(self.wdr)
        workpath = os.path.join(path, "store")
        pth = pathlib.Path(workpath)
        pth.mkdir(parents=True, exist_ok=True)
        modpath = os.path.join(path, "mods")
        pth = pathlib.Path(modpath)
        pth.mkdir(parents=True, exist_ok=True)
        filespath = os.path.join(path, "files")
        pth = pathlib.Path(filespath)
        pth.mkdir(parents=True, exist_ok=True)

    def write(self, obj, path="", base="store"):
        "write object to disk."
        with self.lock:
            if path == "":
                path = ident(obj)
            pth = os.path.join(self.wdr, base, path)
            cdir(pth)
            with open(pth, "w", encoding="utf-8") as fpt:
                dump(obj, fpt, indent=4)
            self.cache.sync(path, obj)
            return path

    def workdir(self, path=""):
        "return workdir."
        return os.path.join(self.wdr, path)


"utility"


def cdir(path):
    "create directory."
    pth = pathlib.Path(path)
    if not os.path.exists(pth.parent):
        pth.parent.mkdir(parents=True, exist_ok=True)


def strip(path):
    "strip filename from path."
    return path.split('store')[-1][1:]


"interface"


def __dir__():
    return (
        'Persist',
        'cdir',
        'db',
        'strip'
    )
