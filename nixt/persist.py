# This file is placed in the Public Domain.
# pylint: disable=R0903


"persistence"


import datetime
import json
import os
import pathlib
import threading
import time


from nixt.methods import fqn, search
from nixt.objects import Object, dump, load, update


j    = os.path.join
lock = threading.RLock()


class Cache:

    "cache"

    objs = {}

    @staticmethod
    def add(path, obj):
        "add object to cache."
        Cache.objs[path] = obj

    @staticmethod
    def get(path):
        "return object from cache."
        return Cache.objs.get(path, None)

    @staticmethod
    def update(path, obj):
        "update cached object."
        if not obj:
            return
        if path in Cache.objs:
            update(Cache.objs[path], obj)
        else:
            Cache.add(path, obj)


def cdir(path):
    "create directory."
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def read(obj, path):
    "read object from path."
    with lock:
        with open(path, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex


def write(obj, path=None):
    "write object to path."
    with lock:
        if path is None:
            path = getpath(obj)
        cdir(path)
        with open(path, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        Cache.update(path, obj)
        return path


class Workdir:

    "working directory."

    name = __file__.rsplit(os.sep, maxsplit=2)[-2]
    wdr  = os.path.expanduser(f"~/.{name}")


def getpath(obj):
    "return new path for object."
    return store(ident(obj))


def ident(obj):
    "return timestamped string."
    return j(fqn(obj), *str(datetime.datetime.now()).split())


def long(name):
    "map short name to full qualified name."
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def moddir():
    "return modules directory."
    return j(Workdir.wdr, "mods")


def pidname(name):
    "return pidfile path."
    return j(Workdir.wdr, f"{name}.pid")


def setwd(name, path=""):
    "set working directory."
    path = path or os.path.expanduser(f"~/.{name}")
    Workdir.wdr = path
    skel()


def skel():
    "create directories."
    result = ""
    if not os.path.exists(store()):
        pth = pathlib.Path(store())
        pth.mkdir(parents=True, exist_ok=True)
        pth = pathlib.Path(moddir())
        pth.mkdir(parents=True, exist_ok=True)
        result =  str(pth)
    return result


def store(pth=""):
    "return store path."
    return j(Workdir.wdr, "store", pth)


def strip(pth, nmr=2):
    "strip path."
    return j(pth.split(os.sep)[-nmr:])


def types():
    "return available types."
    skel()
    return os.listdir(store())


def wdr(pth):
    "return working directory."
    return j(Workdir.wdr, pth)


class Find:

    "find"


def find(clz, selector=None, deleted=False, matching=False):
    "locate objects."
    clz = long(clz)
    if selector is None:
        selector = {}
    for pth in fns(clz):
        obj = Cache.get(pth)
        if not obj:
            obj = Object()
            read(obj, pth)
            Cache.add(pth, obj)
        if not deleted and isdeleted(obj):
            continue
        if selector and not search(obj, selector, matching):
            continue
        yield pth, obj


def fns(clz):
    "return matching filenames."
    pth = store(clz)
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        for dname in dirs:
            ddd = j(rootdir, dname)
            for fll in os.listdir(ddd):
                yield j(ddd, fll)


def fntime(daystr):
    "return filename to time."
    datestr = " ".join(daystr.split(os.sep)[-2:])
    datestr = datestr.replace("_", " ")
    if "." in datestr:
        datestr, rest = datestr.rsplit(".", 1)
    else:
        rest = ""
    timed = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
    if rest:
        timed += float("." + rest)
    return float(timed)


def isdeleted(obj):
    "check whether object is deleted."
    return "__deleted__" in dir(obj) and obj.__deleted__


def last(obj, selector=None):
    "return last version of an object."
    if selector is None:
        selector = {}
    result = sorted(find(fqn(obj), selector), key=lambda x: fntime(x[0]))
    res = ""
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        res = inp[0]
    return res


def __dir__():
    return (
        'Cache',
        'Workdir',
        'cdir',
        'find',
        'fntime',
        'j',
        'last',
        'long',
        'pidname',
        'read',
        'setwd',
        'store',
        'strip',
        'types',
        'write'
    )
