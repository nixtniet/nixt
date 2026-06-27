# This file is placed in the Public Domain.


"usefulness"


import datetime
import inspect
import logging
import os
import pathlib
import time


class Md5:

    @classmethod
    def md5(cls, path):
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

    @classmethod
    def dir(cls, path, md5):
        "create a md5 for a directory."
        for fnm in os.listdir(path):
            if not fnm.endswith(".py"):
                continue
            mpath = j(path, fnm)
            with open(mpath, "r", encoding="utf-8") as file:
                md5.update(file.read().encode("utf-8"))

    @classmethod
    def source(cls, src):
        "determine md5 of source code."
        import hashlib
        md5 = hashlib.md5()
        md5.update(src.encode("utf-8"))
        return str(md5.hexdigest())


class Time:

    starttime = time.time()
    times = [
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

    @classmethod
    def date(cls, daystr):
        "date from string."
        daystr = daystr.encode('utf-8', 'replace').decode("utf-8")
        for fmat in cls.times:
            try:
                return time.mktime(time.strptime(daystr, fmat))
            except ValueError:
                pass

    @classmethod
    def elapsed(cls, seconds, short=True):
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

    @classmethod
    def extract(cls, daystr):
        "extract date/time from string."
        daystr = str(daystr)
        res = None
        for word in daystr.split():
            if word.startswith("+"):
                try:
                    return int(word[1:]) + time.time()
                except (ValueError, IndexError):
                    continue
            res = cls.date(word.strip())
            if not res:
                date = datetime.date.fromtimestamp(time.time())
                word = f"{date.year}-{date.month}-{date.day}" + " " + word
                res = cls.date(word.strip())
            if res:
                break
        return res

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
            timd += float("." + rest)
        return float(timd)

    @classmethod
    def timed(cls, datestr):
        "return time from string."
        if not datestr:
            return time.time()
        tme = cls.date(datestr)
        if not tme:
            tme = time.time()
        return tme

    @classmethod
    def today(cls):
        "start of the day."
        return str(datetime.datetime.today()).split()[0]


class Utils:

    @staticmethod
    def cdir(path):
        "create directory."
        if os.path.exists(path):
            return
        pth = pathlib.Path(path)
        if not os.path.exists(pth.parent):
            pth.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def check(path, md5s):
        "check for md5sums in a given path."
        ok = True
        if not os.path.exists(path):
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
        "return classname of an object."
        return obj.__class__.__name__

    @staticmethod
    def listdir(path, ignore=""):
        "list modules in a directory."
        return [
                x[:-3] for x in os.listdir(path)
                if x.endswith(".py") and
                not x.startswith("__") and
                x[:-3] not in Utils.spl(ignore)
               ]

    @staticmethod
    def moddir():
        "return modules directory."
        return os.path.join(os.path.dirname(__spec__.loader.path), "modules")

    @staticmethod
    def modname(obj):
        "return package name of an object."
        return obj.__module__.split(".")[-1]

    @staticmethod
    def pkgdir(obj):
        "return directory in which a module is defined."
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
        "return the source of a module."
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
    def wrapped(func, *args):
        "wrap function in a try/except, silence ctrl-c/ctrl-d."
        try:
            func(*args)
        except (KeyboardInterrupt, EOFError):
            pass
        except Exception as ex:
            logging.exception(ex)
            return False
        return True


def __dir__():
    return (
        'Md5',
        'Time',
        'Utils'
    )
