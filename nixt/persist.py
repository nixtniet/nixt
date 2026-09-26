# This file is placed in the Public Domain.


"path to object cache"


import datetime
import json
import os
import pathlib
import time


from threading import RLock
from typing    import Any, ClassVar, Dict, Generator, List, Set, Tuple, Union


from .encoder import JSON
from .methods import Method
from .objects import Data
from .utility import Utils


Paths = Generator[str, None, None]
Result = Generator[Tuple[str, Any], None, None]
Selector = Union[Dict[str, str], None]


j = os.path.join


class DecodeError(Exception):

    "could not parse input"


class Cache:

    "path object cache"

    paths: ClassVar[Dict[str, Any]] = {}

    @classmethod
    def add(cls, path: str, obj: Any) -> None:
        "put object into cache."
        cls.paths[path] = obj

    @classmethod
    def get(cls, path: str) -> Any:
        "get object from cache."
        return cls.paths.get(path, None)

    @classmethod
    def sync(cls, path: str, obj: Any) -> None:
        "update cached object."
        try:
            Method.update(cls.paths[path], obj)
        except KeyError:
            cls.add(path, obj)


class Disk:

    "read/write disk"

    lock: RLock = RLock()

    @classmethod
    def ident(cls, obj: Any) -> str:
        "return ident string for object."
        return os.path.join(Method.fqn(obj), *str(datetime.datetime.now(tz=None)).split())

    @classmethod
    def read(cls, obj: Any, path: str, base: str = "store") -> bool:
        "read object from path."
        with cls.lock:
            pth = os.path.join(Workdir.wdr, base, path)
            if not os.path.exists(pth):
                return False
            with open(pth, "r", encoding="utf-8") as fpt:
                try:
                    Method.update(obj, JSON.load(fpt))
                except json.decoder.JSONDecodeError as ex:
                    raise DecodeError(Utils.strip(pth)) from ex
            return True

    @classmethod
    def write(cls, obj: Any, path: str = "", base: str = "store") -> str:
        "write object to disk."
        with cls.lock:
            if path == "":
                path = cls.ident(obj)
            pth = os.path.join(Workdir.wdr, base, path)
            Utils.cdir(pth)
            with open(pth, "w", encoding="utf-8") as fpt:
                JSON.dump(obj, fpt, indent=4)
            Cache.sync(path, obj)
            return path


class Locater:

    "find objects"

    lock: RLock = RLock()

    @classmethod
    def attrs(cls, kind: str) -> Set[str]:
        "show attributes for kind of objects."
        result = []
        for _pth, obj in cls.find(kind, nritems=1):
            if not obj:
                continue
            result.extend(Method.keys(obj))
        return set(result)

    @classmethod
    def count(cls, kind: str) -> int:
        "count kinds of objects."
        return len(list(cls.find(kind)))

    @classmethod
    def find(cls,
             kind: str,
             selector: Selector = None,
             removed: bool = False,
             matching: bool = False,
             nritems: int = 0) -> Result:
        "locate objects by matching atributes."
        with cls.lock:
            if selector is None:
                selector = {}
            nrs = 0
            for pth in cls.fns(Workdir.long(kind)):
                obj = Cache.get(pth)
                if not obj:
                    obj = Data()
                    Disk.read(obj, pth)
                    Cache.add(pth, obj)
                if not removed and Method.deleted(obj):
                    continue
                if selector and not Method.search(obj, selector, matching):
                    continue
                if nritems and nrs >= nritems:
                    break
                nrs += 1
                yield (pth, obj)

    @classmethod
    def first(cls, obj: Any, selector: Selector = None) -> str:
        "return first object of a kind."
        if selector is None:
            selector = {}
        result = sorted(
                        cls.find(Method.fqn(obj), selector),
                        key=lambda x: cls.fntime(x[0])
                       )
        res = ""
        if result:
            inp = result[0]
            Method.update(obj, inp[-1])
            res = inp[0]
        return res

    @classmethod
    def fns(cls, kind: str) -> Paths:
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
    def fntime(cls, daystr: str) -> float:
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
    def last(cls, obj: Any, selector=None) -> str:
        "last saved version."
        if selector is None:
            selector = {}
        result = sorted(
                        cls.find(Method.fqn(obj), selector),
                        key=lambda x: cls.fntime(x[0])
                       )
        res = ""
        if result:
            inp = result[-1]
            Method.update(obj, inp[-1])
            res = inp[0]
        return res

    @classmethod
    def strip(cls, path: str) -> str:
        "strip filename from path."
        return path.split('store')[-1][1:]


class Workdir:

    "the store everything directory"

    wdr = ""

    @classmethod
    def home(cls, name: str) -> str:
        "return home working directory."
        return os.path.expanduser(f"~/.{name}")

    @classmethod
    def kinds(cls) -> List[str]:
        "show kind on objects in cache."
        assert cls.wdr
        path = j(cls.wdr, "store")
        if not os.path.exists(path):
            cls.skel()
        return os.listdir(path)

    @classmethod
    def logdir(cls, path: str = "") -> str:
        "return directory to logs."
        assert cls.wdr
        return j(cls.wdr, "logs", path)

    @classmethod
    def long(cls, name: str) -> str:
        "expand to fqn."
        if "." in name:
            return name
        split = name.split(".")[-1].lower()
        res = name
        for names in cls.kinds():
            if split == names.split(".")[-1].lower():
                res = names
                break
        return res

    @classmethod
    def moddir(cls) -> str:
        "return modules directory."
        assert cls.wdr
        return j(cls.wdr, "mods")

    @classmethod
    def pid(cls, name: str) -> None:
        "write pid to file."
        assert cls.wdr
        filename = j(cls.wdr, f"{name}.pid")
        if os.path.exists(filename):
            os.unlink(filename)
        path2 = pathlib.Path(filename)
        path2.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as fds:
            fds.write(str(os.getpid()))

    @classmethod
    def skel(cls) -> None:
        "create directories."
        assert cls.wdr
        if not os.path.exists(cls.wdr):
            Utils.cdir(cls.wdr)
        path = os.path.abspath(cls.wdr)
        for wpth in ["config", "logs", "mods", "store"]:
            pth = pathlib.Path(j(path, wpth))
            pth.mkdir(parents=True, exist_ok=True)


def __dir__():
    return (
        'Disk',
        'Locater',
        'WOrkdir'
    )
