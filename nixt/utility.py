# This file is placed in the Public Domain.


"usefulness"


import datetime
import inspect
import logging
import os
import pathlib
import time


a = os.path.abspath
d = os.path.dirname
e = os.path.exists
i = os.path.isfile
j = os.path.join


class Md5:

    @staticmethod
    def md5(path):
        "calculate md5sum of a file."
        import hashlib
        md5 = hashlib.md5()
        with open(path, "r", encoding="utf-8") as file:
            md5.update(file.read().encode("utf-8"))
        return str(md5.hexdigest())

    @classmethod
    def core(cls):
        "calculate md5 of the statics module."
        try:
            from . import statics
        except (ModuleNotFoundError, ImportError, SyntaxError):
            return ""
        return cls.source(Utils.source(statics))[:7].upper()

    @staticmethod
    def dir(path, md5):
        "create a md5 for a directory."
        for fnm in os.listdir(path):
            if not fnm.endswith(".py"):
                continue
            mpath = j(path, fnm)
            with open(mpath, "r", encoding="utf-8") as file:
                md5.update(file.read().encode("utf-8"))

    @staticmethod
    def source(src):
        "determine md5 of source code."
        import hashlib
        md5 = hashlib.md5()
        md5.update(src.encode("utf-8"))
        return str(md5.hexdigest())


class Time:

    starttime = time.time()

    @staticmethod
    def date(daystr):
        "date from string."
        daystr = daystr.encode('utf-8', 'replace').decode("utf-8")
        for fmat in TIMES:
            try:
                return time.mktime(time.strptime(daystr, fmat))
            except ValueError:
                pass

    @staticmethod
    def elapsed(seconds, short=True):
        "seconds to string."
        txt = ""
        nsec = float(seconds)
        if nsec < 1:
            return f"{nsec:.2f}s"
        yea = 365 * 24 * 60 * 60
        week = 7 * 24 * 60 * 60
        nday = 24 * 60 * 60
        hou = 60 * 60
        minute = 60
        yeas = int(nsec / yea)
        nsec -= yeas * yea
        weeks = int(nsec / week)
        nsec -= weeks * week
        nrdays = int(nsec / nday)
        nsec -= nrdays * nday
        hours = int(nsec / hou)
        nsec -= hours * hou
        minutes = int(nsec / minute)
        nsec -= minutes * minute
        sec = int(nsec / 1)
        nsec -= nsec - sec
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

    @staticmethod
    def extract(daystr):
        "extract date/time from string."
        daystr = str(daystr)
        res = None
        for word in daystr.split():
            if word.startswith("+"):
                try:
                    return int(word[1:]) + time.time()
                except (ValueError, IndexError):
                    continue
            res = Time.date(word.strip())
            if not res:
                date = datetime.date.fromtimestamp(time.time())
                word = f"{date.year}-{date.month}-{date.day}" + " " + word
                res = Time.date(word.strip())
            if res:
                break
        return res

    @staticmethod
    def fntime(daystr):
        "time from path."
        datestr = " ".join(daystr.split(os.sep)[-2:])
        datestr = datestr.replace("_", " ")
        if "." in datestr:
            datestr, rest = datestr.rsplit(".", 1)
        else:
            rest = ""
        timd = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
        if rest:
            timd += float("." + rest)
        return float(timd)

    @staticmethod
    def timed(datestr):
        "return time from string."
        if not datestr:
            return time.time()
        tme = Time.date(datestr)
        if not tme:
            tme = time.time()
        return tme

    @staticmethod
    def today():
        "start of the day."
        return str(datetime.datetime.today()).split()[0]


class Utils:

    @staticmethod
    def cdir(path):
        "create directory."
        if e(path):
            return
        pth = pathlib.Path(path)
        if not e(pth.parent):
            pth.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def check(path, md5s):
        "check for md5sums in a given path."
        ok = True
        if not e(path):
            return False
        for pth in os.listdir(path):
            if pth.startswith("__") or not pth.endswith(".py") or "statics" in pth:
                continue
            name = pth[:-3]
            modpath = j(path, pth)
            if Md5.md5(modpath) != md5s.get(name):
                logging.warning("mismatch %s", name)
                ok = False
        return ok

    @staticmethod
    def clsname(obj):
        "reutrn classname of an object."
        return obj.__class__.__name__

    @staticmethod
    def html(text):
        "wrap text as html."
        return """<!doctype html>\n<html>   %s\n</html>""" % text

    @staticmethod
    def listdir(path, ignore=""):
        return [
                x[:-3] for x in os.listdir(path)
                if x.endswith(".py") and
                not x.startswith("__") and
                x[:-3] not in Utils.spl(ignore)
               ]

    @staticmethod
    def moddir():
        "return modules directory."
        return j(os.path.dirname(__spec__.loader.path), "modules")

    @staticmethod
    def modname(obj):
        "return package name of an object."
        return obj.__module__.split(".")[-1]

    @staticmethod
    def pkgdir(obj):
        return d(inspect.getfile(obj))

    @staticmethod
    def pkgname(obj):
        "return package name of an object."
        return obj.__module__.split(".", maxsplit=1)[0]

    @staticmethod
    def pipxdir(name):
        "return examples directory."
        return f"~/.local/share/pipx/venvs/{name}/share/{name}/"

    @staticmethod
    def skip(obj):
        "skip underscore keys."
        result = []
        for x in dir(obj):
            if x.startswith("_"):
                continue
            result.append(x)
        return sorted(result)

    @staticmethod
    def skipped(obj):
        "yield without underscore values."
        for key in dir(obj):
            if key.startswith("_"):
                continue
            yield getattr(obj, key)

    @staticmethod
    def source(module):
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
    def where(obj):
        "path where object is defined."
        return os.path.dirname(inspect.getfile(obj))

    @staticmethod
    def wrapped(func):
        "wrap function in a try/except, silence ctrl-c/ctrl-d."
        try:
            func()
        except (KeyboardInterrupt, EOFError):
            pass


TIMES = [
    "%a, %d %b %Y %H:%M:%S %z",
    "%a, %d %b %Y %H:%M:%S",
    "%a, %d %b %Y %T %z",
    "%a, %d %b %Y %T",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%d-%m",
    "%m-%d"
]


def __dir__():
    return (
        'Times',
        'Md5',
        'Time',
        'Utils',
        'a',
        'd',
        'e',
        'j'
    )
