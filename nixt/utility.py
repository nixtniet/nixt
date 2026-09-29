# This file is placed in the Public Domain.


"usefullness"


import datetime
import os
import pathlib
import time
import uuid


from .typings import Any, ClassVar, Float, List, ModuleType, Union


class Time:

    "time related utilities."

    starttime: ClassVar[float] = time.time()
    times = (
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
    )

    @classmethod
    def date(cls, daystr: str) -> Float:
        "date from string."
        daystr = daystr.encode('utf-8', 'replace').decode("utf-8")
        for fmat in cls.times:
            try:
                return time.mktime(time.strptime(daystr, fmat))
            except ValueError:
                pass
        return None

    @classmethod
    def elapsed(cls, seconds: float, short: bool = True) -> str:
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
    def extract(cls, daystr: str) -> Float:
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
                date = datetime.datetime.fromtimestamp(time.time(), tz=None).date()
                word = f"{date.year}-{date.month}-{date.day}" + " " + word
                res = cls.date(word.strip())
            if res:
                break
        return res

    @classmethod
    def timed(cls, datestr: str) -> float:
        "return time from string."
        if not datestr:
            return time.time()
        tme = cls.date(datestr)
        if not tme:
            tme = time.time()
        return tme


class Utils:

    "useful functions"

    @staticmethod
    def cdir(path: str) -> None:
        "create directory."
        if os.path.exists(path):
            return
        pth = pathlib.Path(path)
        if not os.path.exists(pth.parent):
            pth.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def clsname(obj: Any) -> str:
        "return classname of an object."
        return obj.__class__.__name__

    @staticmethod
    def home(name: str) -> str:
        "return home working directory."
        return os.path.expanduser(f"~/.{name}")

    @staticmethod
    def listdir(path: str, ignore: str = "") -> List[str]:
        "list modules in a directory."
        return [
                x[:-3] for x in os.listdir(path)
                if x.endswith(".py") and
                not x.startswith("__") and
                x[:-3] not in Utils.spl(ignore)
               ]

    @staticmethod
    def shortid() -> str:
        "return a shortid."
        return str(uuid.uuid4())[:8]

    @staticmethod
    def source(module: ModuleType) -> Union[str, None]:
        "return the source of a module."
        if module.__spec__ is None:
            return None
        if module.__spec__.loader is None:
            return None
        get = getattr(module.__spec__.loader, "get_source", None)
        if get:
            return get(module.__name__)
        return None

    @staticmethod
    def spl(text: str, ignore: str = "") -> List[str]:
        "list from comma seperated string."
        try:
            ignores = ignore.split(",")
            result = text.split(",")
        except (TypeError, ValueError):
            result = []
        return [x for x in result if x and x not in ignores]

    @staticmethod
    def strip(path: str, nrchar: int = 3) -> str:
        "strip filename from path."
        return os.path.join(*path.split(os.sep)[-nrchar:])


def __dir__():
    return (
        'Time',
        'Utils'
    )
