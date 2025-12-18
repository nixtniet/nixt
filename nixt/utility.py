# This file is placed in the Public Domain.


"dumpyard"


import datetime
import importlib.util
import inspect
import os
import pathlib
import re
import time


from .methods import Method
from .objects import Dict
from .statics import Static


class NoDate(Exception):

    pass


class Time:

    @staticmethod
    def date(daystr):
        daystr = daystr.encode('utf-8', 'replace').decode("utf-8")
        res = time.time()
        for fmat in Static.TIMES:
            try:
                res = time.mktime(time.strptime(daystr, fmat))
                break
            except ValueError:
                pass
        return res

    @staticmethod
    def day(daystr):
        day = None
        month = None
        yea = None
        try:
            ymdre = re.search(r'(\d+)-(\d+)-(\d+)', daystr)
            if ymdre:
                (day, month, yea) = ymdre.groups()
        except ValueError:
            try:
                ymre = re.search(r'(\d+)-(\d+)', daystr)
                if ymre:
                    (day, month) = ymre.groups()
                    yea = time.strftime("%Y", time.localtime())
            except Exception as ex:
                raise NoDate(daystr) from ex
        if day:
            day = int(day)
            month = int(month)
            yea = int(yea)
            date = f"{day} {Static.MONTH[month]} {yea}"
            return time.mktime(time.strptime(date, r"%d %b %Y"))
        raise NoDate(daystr)

    @staticmethod
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

    @staticmethod
    def extract(daystr):
        previous = ""
        line = ""
        daystr = str(daystr)
        res = None
        for word in daystr.split():
            line = previous + " " + word
            previous = word
            try:
                res = Utils.extractdate(line.strip())
                break
            except ValueError:
                res = None
            line = ""
        return res

    @staticmethod
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

    @staticmethod
    def hour(daystr):
        try:
            hmsre = re.search(r'(\d+):(\d+):(\d+)', str(daystr))
            hours = 60 * 60 * (int(hmsre.group(1)))
            hoursmin = hours  + int(hmsre.group(2)) * 60
            hmsres = hoursmin + int(hmsre.group(3))
        except AttributeError:
            pass
        except ValueError:
            pass
        try:
            hmre = re.search(r'(\d+):(\d+)', str(daystr))
            hours = 60 * 60 * (int(hmre.group(1)))
            hmsres = hours + int(hmre.group(2)) * 60
        except AttributeError:
            return 0
        except ValueError:
           return 0
        return hmsres

    @staticmethod
    def time(txt):
        try:
            target = Time.day(txt)
        except NoDate:
            target = Time.extract(Time.today())
        hour =  Time.hour(txt)
        if hour:
            target += hour
        return target

    @staticmethod
    def parse(txt):
        seconds = 0
        target = 0
        txt = str(txt)
        for word in txt.split():
            if word.startswith("+"):
                seconds = int(word[1:])
                return time.time() + seconds
            if word.startswith("-"):
                seconds = int(word[1:])
                return time.time() - seconds
        if not target:
            try:
                target = Time.day(txt)
            except NoDate:
               target = Time.extract(Time.today())
            hour = Time.hour(txt)
            if hour:
                target += hour
        return target

    @staticmethod
    def today():
        return str(datetime.datetime.today()).split()[0]


class Utils:

    @staticmethod
    def cdir(path):
        pth = pathlib.Path(path)
        pth.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def expand(cls, keys=None):
        #stack = inspect.stack(1)[1]
        #context = stack.code_context[0]
        #print(dir(stack.frame))
        for key, value in Dict.items(cls):
            if keys and key not in Utils.spl(keys):
                continue
            inspect.stack(1)[1].frame.f_globals[key] = value

    @staticmethod
    def ident(obj):
        return os.path.join(Method.fqn(obj), *str(datetime.datetime.now()).split())

    @staticmethod
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

    @staticmethod
    def md5sum(path):
        import hashlib
        with open(path, "r", encoding="utf-8") as file:
            txt = file.read().encode("utf-8")
            return hashlib.md5(txt, usedforsecurity=False).hexdigest()

    @staticmethod
    def spl(txt):
        try:
           result = txt.split(",")
        except (TypeError, ValueError):
           result = []
        return [x for x in result if x]

    @staticmethod
    def where(obj):
        return os.path.dirname(inspect.getfile(obj))


def __dir__():
    return (
        'Time',
        'Utils'
    )
