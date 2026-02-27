# This file is placed in the Public Domain.


"persistence through storage"


import json
import os
import pathlib
import threading


from .encoder import Json
from .objects import Configuration, Default, Dict, Methods, Static
from .utility import Time, Utils


class Main(Configuration):

    debug = False
    level = "info"
    name = Utils.pkgname(Configuration)
    version = 1
    wdr = f".{name}"


class Cache:

    __metaclass__ = Static

    paths = {}

    def add(path, obj):
        "put object into cache."
        Cache.paths[path] = obj

    def get(path):
        "get object from cache."
        return Cache.paths.get(path, None)

    def sync(path, obj):
        "update cached object."
        try:
            Dict.update(Cache.paths[path], obj)
        except KeyError:
            Cache.add(path, obj)


class Disk:

    __metaclass__ = Static

    lock = threading.RLock()

    def cdir(path):
        "create directory."
        pth = pathlib.Path(path)
        if not os.path.exists(pth.parent):
            pth.parent.mkdir(parents=True, exist_ok=True)

    def read(obj, path, base="store"):
        "read object from path."
        with Disk.lock:
            pth = os.path.join(Main.wdr, base, path)
            if not os.path.exists(pth):
                return
            with open(pth, "r", encoding="utf-8") as fpt:
                try:
                    Dict.update(obj, Json.load(fpt))
                except json.decoder.JSONDecodeError as ex:
                    ex.add_note(path)
                    raise ex

    def write(obj, path="", base="store"):
        "write object to disk."
        with Disk.lock:
            if path == "":
                path = Methods.ident(obj)
            pth = os.path.join(Main.wdr, base, path)
            Disk.cdir(pth)
            with open(pth, "w", encoding="utf-8") as fpt:
                Json.dump(obj, fpt, indent=4)
            Cache.sync(path, obj)
            return path


class Locate:

    __metaclass__ = Static

    def attrs(kind):
        "show attributes for kind of objects."
        result = []
        for pth, obj in Locate.find(kind, nritems=1):
            result.extend(Dict.keys(obj))
        return {x for x in result}

    def count(kind):
        return len(list(Locate.find(kind)))

    def find(kind, selector={}, removed=False, matching=False, nritems=None):
        "locate objects by matching atributes."
        nrs = 0
        for pth in Locate.fns(Workdir.long(kind)):
            obj = Cache.get(pth)
            if not obj:
                obj = Default()
                Disk.read(obj, pth)
                Cache.add(pth, obj)
            if not removed and Methods.deleted(obj):
                continue
            if selector and not Methods.search(obj, selector, matching):
                continue
            if nritems and nrs >= nritems:
                break
            nrs += 1
            yield pth, obj
        else:
            return None, None

    def first(obj, selector={}):
        result = sorted(
                        Locate.find(Methods.fqn(obj), selector),
                        key=lambda x: Time.fntime(x[0])
                       )
        res = ""
        if result:
            inp = result[0]
            Dict.update(obj, inp[-1])
            res = inp[0]
        return res

    def fns(kind):
        "file names by kind of object."
        path = os.path.join(Main.wdr, "store", kind)
        for rootdir, dirs, _files in os.walk(path, topdown=True):
            for dname in dirs:
                if dname.count("-") != 2:
                    continue
                ddd = os.path.join(rootdir, dname)
                for fll in os.listdir(ddd):
                    yield Locate.strip(os.path.join(ddd, fll))

    def last(obj, selector={}):
        "last saved version."
        result = sorted(
                        Locate.find(Methods.fqn(obj), selector),
                        key=lambda x: Time.fntime(x[0])
                       )
        res = ""
        if result:
            inp = result[-1]
            Dict.update(obj, inp[-1])
            res = inp[0]
        return res

    def strip(path):
        "strip filename from path."
        return path.split('store')[-1][1:]


class StateFul:

    def __init__(self):
        super().__init__()
        self.fnm = ""

    def dump(self):
        if not self.fnm:
            self.fnm = Locate.first(self) or Methods.ident(self)
        Disk.write(self, self.fnm)
    
    def load(self):
        Locate.first(self)


class Workdir:

    __metaclass__ = Static

    def kinds():
        "show kind on objects in cache."
        return os.listdir(os.path.join(Main.wdr, "store"))

    def long(name):
        "expand to fqn."
        if "." in name:
            return name
        split = name.split(".")[-1].lower()
        res = name
        for names in Workdir.kinds():
            if split == names.split(".")[-1].lower():
                res = names
                break
        return res

    def pidfile(name):
        "write pidfile."
        filename = os.path.join(Main.wdr, f"{name}.pid")
        if os.path.exists(filename):
            os.unlink(filename)
        path2 = pathlib.Path(filename)
        path2.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as fds:
            fds.write(str(os.getpid()))

    def skel():
        "create directories."
        if not Main.wdr:
            return
        path = os.path.abspath(Main.wdr)
        workpath = os.path.join(path, "store")
        pth = pathlib.Path(workpath)
        pth.mkdir(parents=True, exist_ok=True)
        modpath = os.path.join(path, "mods")
        pth = pathlib.Path(modpath)
        pth.mkdir(parents=True, exist_ok=True)
        filespath = os.path.join(path, "files")
        pth = pathlib.Path(filespath)
        pth.mkdir(parents=True, exist_ok=True)

    def setwd(path):
        "enable writing to disk."
        Main.wdr = path
        Workdir.skel()

    def workdir(path=""):
        "return workdir."
        return os.path.join(Main.wdr, path)


def __dir__():
    return (
        'Disk',
        'Locate',
        'Main',
        'StateFul',
        'Workdir'
    )
