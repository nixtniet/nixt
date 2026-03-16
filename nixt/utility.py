# This file is placed in the Public Domain.


"usefulness"


import datetime
import inspect
import os
import time


class NoDate(Exception):

    pass


class Time:

    @classmethod
    def date(cls, daystr):
        "date from string."
        daystr = daystr.encode('utf-8', 'replace').decode("utf-8")
        if "-" not in daystr:
            date = datetime.date.fromtimestamp(time.time())
            daystr = f"{date.year}-{date.month}-{date.day}" + " " + daystr
        for fmat in TIMES:
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
            try:
                res = cls.date(word.strip())
                break
            except ValueError:
                res = None
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
    def today(cls):
        "start of the day."
        return str(datetime.datetime.today()).split()[0]


class Utils:

    @staticmethod
    def md5sum(path):
        "return md5 of a file."
        import hashlib
        if not os.path.exists(path):
            return ""
        with open(path, "r", encoding="utf-8") as file:
            txt = file.read().encode("utf-8")
            return hashlib.md5(txt, usedforsecurity=False).hexdigest()  # pylint: disable=E1123

    @staticmethod
    def md5s(path):
        import hashlib
        sums = hashlib.md5(usedforsecurity=False)  # pylint: disable=E1123
        for fnm in os.listdir(path):
            if fnm.startswith("_"):
                continue
            pth = os.path.join(path, fnm)
            with open(pth, "rb") as file:
                sums.update(file.read())
        return sums.hexdigest()

    @staticmethod
    def pkgname(obj):
        "return package name of an object."
        return obj.__module__.split(".", maxsplit=1)[0]

    @staticmethod
    def pipxdir(name):
        "return examples directory."
        return f"~/.local/share/pipx/venvs/{name}/share/{name}/"

    @staticmethod
    def spl(txt):
        "list from comma seperated string."
        try:
            result = txt.split(",")
        except (TypeError, ValueError):
            result = []
        return [x for x in result if x]

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


SYSTEMD = """[Unit]
Description=%s
After=multi-user.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%s -s

[Install]
WantedBy=multi-user.target"""


TIMES = [
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
        'SYSTEMD',
        'Log',
        'NoDate',
        'Time',
        'Utils'
    )
