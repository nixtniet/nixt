# This file is placed in the Public Domain.


"path to object cache"


import datetime
import json
import os
import time
import types


from .configs import Main
from .encoder import JSON
from .functio import Dicts
from .generic import Path, RLock
from .methods import Methods
from .utility import Log, Utils


logger = Log(__name__)


class DecodeError(Exception):

    "could not parse to JSON"


class MissingPath(Exception):

    "don't know where to write"


class Cache:

    "path object cache"

    paths = {}

    @classmethod
    def add(cls, path, obj):
        "put object into cache."
        if not isinstance(obj, (dict, types.MappingProxyType)):
            raise TypeError(type(obj))
        cls.paths[path] = obj

    @classmethod
    def get(cls, path):
        "get object from cache."
        return cls.paths.get(path, None)

    @classmethod
    def sync(cls, path, obj):
        "update cached object."
        try:
            cls.paths[path].update(obj)
        except (KeyError, AttributeError):
            cls.add(path, obj)


class Disk:

    "read/write disk"

    lock = RLock()

    @classmethod
    def cdir(cls, path):
        "create directory."
        if os.path.exists(path):
            return
        with cls.lock:
            pth = Path(path)
            if not os.path.exists(pth.parent):
                pth.parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def ident(cls, clz):
        "return ident string for object."
        return os.path.join(Methods.fqn(clz), *str(datetime.datetime.now(tz=None)).split())

    @classmethod
    def read(cls, path, base="store"):
        "read object from path."
        with cls.lock:
            pth = os.path.join(Workdir.wdr, base, path)
            logger.debug("read %s/%s", base, path)
            if not os.path.exists(pth):
                return {}
            with open(pth, "r", encoding="utf-8") as fpt:
                try:
                    return JSON.load(fpt)
                except json.JSONDecodeError as ex:
                    raise DecodeError(Utils.strip(pth)) from ex

    @classmethod
    def write(cls, dct,  path, base="store"):
        "write object to disk."
        if not path:
            raise MissingPath
        with cls.lock:
            pth = os.path.join(Workdir.wdr, base, path)
            logger.debug("write %s/%s", base, path)
            cls.cdir(pth)
            with open(pth, "w", encoding="utf-8") as fpt:
                JSON.dump(dct, fpt, indent=4)
            Cache.sync(path, dct)
            return path


class Dump:

    "state of wisdom"

    def __init__(self):
        super().__init__()
        self.fnm = ""

    def dump(self):
        "dump state to disk."
        if not self.fnm:
            self.fnm, _x = Locater.first(Methods.fqn(self))
        if not self.fnm:
            self.fnm = Disk.ident(self)
        Disk.write(vars(self), self.fnm)

    def load(self):
        "load from disk."
        _path, dct = Locater.first(Methods.fqn(self))
        if dct:
            Methods.update(self, dct)


class Locater:

    "find objects"

    lock = RLock()

    @classmethod
    def attrs(cls, kind):
        "show attributes for kind of objects."
        _pth, obj = cls.first(kind)
        if obj:
            return obj.keys()
        return []

    @classmethod
    def count(cls, kind):
        "count kinds of objects."
        return len(list(cls.find(kind)))

    @classmethod
    def find(cls, kind, selector=None, removed=False, matching=False):
        "locate objects by matching atributes."
        if selector is None:
            selector = {}
        for pth in cls.fns(Workdir.long(kind)):
            dct = Cache.get(pth)
            if not dct:
                dct = Disk.read(pth)
                Cache.add(pth, dct)
            if not removed and Dicts.deleted(dct):
                continue
            if selector and not Dicts.search(dct, selector, matching):
                continue
            yield (pth, dct)

    @classmethod
    def first(cls, kind, selector=None):
        "return first object of a kind."
        result = sorted(
                        cls.find(kind, selector),
                        key=lambda x: cls.fntime(x[0])
                       )
        if result:
            return result[0]
        return (None, None)

    @classmethod
    def fns(cls, kind):
        "file names by kind of object."
        path = os.path.join(Workdir.wdr, "store", kind)
        for rootdir, dirs, _files in os.walk(path, topdown=True):
            for dname in dirs:
                if dname.count("-") != 2:
                    continue
                ddd = os.path.join(rootdir, dname)
                for fll in os.listdir(ddd):
                    yield cls.strip(os.path.join(ddd, fll))

    @classmethod
    def fntime(cls, daystr):
        "time from path."
        datestr = " ".join(daystr.split(os.sep)[-2:])
        datestr = datestr.replace("_", " ")
        if "." in datestr:
            datestr, rest = datestr.rsplit(".", 1)
        else:
            rest = ""
        timd = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
        if rest:
            try:
                timd += float("." + rest)
            except ValueError:
                pass
        return float(timd)

    @classmethod
    def last(cls, kind, selector=None):
        "last saved version."
        result = sorted(
            cls.find(kind, selector),
            key=lambda x: cls.fntime(x[0])
        )
        if result:
            return result[-1]
        return (None, None)

    @classmethod
    def objects(cls, kind, selector=None, removed=False, matching=False):
        "return objects by matching atributes."
        yield from [x[1] for x in cls.find(
            kind,
            selector,
            removed,
            matching
        )]

    @classmethod
    def strip(cls, path):
        "strip filename from path."
        return path.rsplit('store', maxsplit=1)[-1][1:]


class Workdir:

    "the store everything directory"

    wdr = ""

    @classmethod
    def configure(cls, wdr=None):
        "configure storage path."
        cls.wdr = wdr or Main.wdr or cls.wdr or cls.home(Main.name)
        cls.skel()

    @classmethod
    def home(cls, name):
        "return home working directory."
        return os.path.expanduser(f"~/.{name}")

    @classmethod
    def kinds(cls):
        "show kind on objects in cache."
        assert cls.wdr
        path = os.path.join(cls.wdr, "store")
        if not os.path.exists(path):
            cls.skel()
        return os.listdir(path)

    @classmethod
    def logdir(cls, path=""):
        "return directory to logs."
        assert cls.wdr
        return os.path.join(cls.wdr, "logs", path)

    @classmethod
    def long(cls, name):
        "expand to fqn."
        if "." in name:
            return name
        split = name.rsplit(".", maxsplit=1)[-1].lower()
        res = name
        for names in cls.kinds():
            if split == names.split(".")[-1].lower():
                res = names
                break
        return res

    @classmethod
    def moddir(cls):
        "return modules directory."
        assert cls.wdr
        return os.path.join(cls.wdr, "mods")

    @classmethod
    def pid(cls, name):
        "write pid to file."
        assert cls.wdr
        filename = os.path.join(cls.wdr, f"{name}.pid")
        if os.path.exists(filename):
            os.unlink(filename)
        path2 = Path(filename)
        path2.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as fds:
            fds.write(str(os.getpid()))

    @classmethod
    def skel(cls):
        "create directories."
        assert cls.wdr
        if not os.path.exists(cls.wdr):
            Disk.cdir(cls.wdr)
        path = os.path.abspath(cls.wdr)
        for wpth in ["config", "logs", "mods", "store"]:
            pth = Path(os.path.join(path, wpth))
            pth.mkdir(parents=True, exist_ok=True)


def __dir__():
    return (
        'Disk',
        'Dump',
        'Locater',
        'Selector',
        'Workdir'
    )
