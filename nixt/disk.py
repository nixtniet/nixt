# This file is placed in the Public Domain.


"cache"


import datetime
import json
import os
import pathlib
import threading
import time


from .object import Object, dump, load, update


lock = threading.RLock()
p    = os.path.join


class Workdir:

    name = __file__.rsplit(os.sep, maxsplit=2)[-2]
    wdr = ""


class Cache:

    disk = False
    objs = {}
    types = []

    @staticmethod
    def add(path, obj):
        Cache.objs[path] = obj
        typ = fqn(obj)
        if typ not in Cache.types:
            Cache.types.append(typ)

    @staticmethod
    def get(path):
        return Cache.objs.get(path, None)

    @staticmethod
    def typed(typ):
        return [x for x in Cache.objs.keys() if typ in x]

    @staticmethod
    def update(path, obj):
        if not obj:
            return
        if path in Cache.objs:
            update(Cache.objs[path], obj)
        else:
            Cache.add(path, obj)


def cdir(path):
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def find(clz, selector=None, deleted=False, matching=False, disk=False):
    if selector is None:
        selector = {}
    if disk or Cache.disk:
        paths = sorted(fns(clz))
    else:
        paths = Cache.typed(long(clz))
    for pth  in paths:
        ppth = strip(pth)
        if clz not in ppth:
            continue
        obj = Cache.get(ppth)
        if not obj:
            obj = Object()
            read(obj, ppth)
            Cache.add(ppth, obj)
        if not deleted and isdeleted(obj):
            continue
        if selector and not search(obj, selector, matching):
            continue
        yield ppth, obj


def fns(clz):
    dname = ''
    pth = store(long(clz))
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        if dirs:
            for dname in sorted(dirs):
                if dname.count('-') == 2:
                    ddd = p(rootdir, dname)
                    for fll in os.listdir(ddd):
                        yield p(ddd, fll)


def fntime(daystr):
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


def fqn(obj):
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def getpath(obj):
    return ident(obj)


def ident(obj):
    return os.path.join(fqn(obj), *str(datetime.datetime.now()).split())


def isdeleted(obj):
    return "__deleted__" in dir(obj) and obj.__deleted__


def last(obj, selector=None):
    if selector is None:
        selector = {}
    result = sorted(find(fqn(obj), selector), key=lambda x: fntime(x[0]))
    res = ""
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        res = inp[0]
    return res


def long(name):
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def read(obj, path, disk=False):
    with lock:
        try:
            if disk or Cache.disk:
                ppath = store(path)
                with open(ppath, "r", encoding="utf-8") as fpt:
                    update(obj, load(fpt))
                Cache.update(path, obj)
            else:
                update(obj, Cache.get(path))
        except json.decoder.JSONDecodeError as ex:
            ex.add_note(path)
            raise ex

 
def search(obj, selector, matching=False):
    res = False
    if not selector:
        return res
    for key, value in selector.items():
        val = getattr(obj, key, None)
        if not val:
            continue
        if matching and value == val:
            res = True
        elif str(value).lower() in str(val).lower() or value == "match":
            res = True
        else:
            res = False
            break
    return res


def skel():
    pth = pathlib.Path(store())
    pth.mkdir(parents=True, exist_ok=True)
    return str(pth)


def store(pth=""):
    return os.path.join(Workdir.wdr, "store", pth)


def strip(pth, nmr=3):
    return os.sep.join(pth.split(os.sep)[-nmr:])


def types() -> [str]:
    return os.listdir(store())


def write(obj, path, disk=False):
    with lock:
        if disk or Cache.disk:
            ppath = store(path)
            cdir(ppath)
            with open(ppath, "w", encoding="utf-8") as fpt:
                dump(obj, fpt, indent=4)
        Cache.update(path, obj)
        return path


def __dir__():
    return (
        'Cache',
        'read',
        'write'
    )
