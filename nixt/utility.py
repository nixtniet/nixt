# This file is placed in the Public Domain.


"dumpyard"


import importlib.util
import inspect
import os
import time


from nixt.objects import Object
from nixt.statics import TIMES


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


def elapsed(seconds, short=True):
    txt = ""
    nsec = float(seconds)
    if nsec < 1:
        return f"{nsec:.2f}s"
    yea     = 365 * 24 * 60 * 60
    week    = 7 * 24 * 60 * 60
    nday    = 24 * 60 * 60
    hour    = 60 * 60
    minute  = 60
    yeas    = int(nsec / yea)
    nsec   -= yeas * yea
    weeks   = int(nsec / week)
    nsec   -= weeks * week
    nrdays  = int(nsec / nday)
    nsec   -= nrdays * nday
    hours   = int(nsec / hour)
    nsec   -= hours * hour
    minutes = int(nsec / minute)
    nsec   -= minutes * minute
    sec     = int(nsec / 1)
    nsec   -= nsec - sec
    if yeas:
        txt += f"{yeas}y"
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += f"{nrdays}d"
    if hours:
        txt += f"{hours}h"
    if short and txt:
        return txt.strip()
    if minutes:
        txt += f"{minutes}m"
    if sec:
        txt += f"{sec}s"
    txt = txt.strip()
    return txt


def extract_date(daystr):
    daystr = daystr.encode('utf-8', 'replace').decode("utf-8")
    res = time.time()
    for fmat in TIMES:
        try:
            res = time.mktime(time.strptime(daystr, fmat))
            break
        except ValueError:
            pass
    return res


def importer(name, pth=""):
    if pth and os.path.exists(pth):
        spec = importlib.util.spec_from_file_location(name, pth)
    else:
        spec = importlib.util.find_spec(name)
    if not spec or not spec.loader:
        return None
    mod = importlib.util.module_from_spec(spec)
    if not mod:
        return None
    spec.loader.exec_module(mod)
    return mod


def md5sum(path):
    import hashlib
    with open(path, "r", encoding="utf-8") as file:
        txt = file.read().encode("utf-8")
        return hashlib.md5(txt, usedforsecurity=False).hexdigest()


def spl(txt):
    try:
        result = txt.split(",")
    except (TypeError, ValueError):
        result = []
    return [x for x in result if x]


def where(obj):
     return os.path.dirname(inspect.getfile(obj))


def wrapped(func):
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        pass


def __dir__():
    return (
        'elapsed',
        'extract_date',
        'importer',
        'md5sum',
        'spl',
        'where',
        'wrapped'
    )
