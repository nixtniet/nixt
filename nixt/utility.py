# This file is placed in the Public Domain.


"dumpyard"


import datetime
import inspect
import os
import pathlib
import re
import time


from .methods import fqn
from .statics import MONTH, TIMES


class NoDate(Exception):

    pass


def cdir(path):
    "create directory."
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def ident(obj):
    "return ident string for object."
    return os.path.join(fqn(obj), *str(datetime.datetime.now()).split())


def md5sum(path):
    "return md5 of a file."
    import hashlib
    with open(path, "r", encoding="utf-8") as file:
        txt = file.read().encode("utf-8")
        return hashlib.md5(txt, usedforsecurity=False).hexdigest()


def spl(txt):
    "return list from command seperated string."
    try:
        result = txt.split(",")
    except (TypeError, ValueError):
        result = []
    return [x for x in result if x]


def where(obj):
    "return path where object is defined."
    return os.path.dirname(inspect.getfile(obj))


def wrapped(func):
    "wrap function in a try/except, silence ctrl-c/ctrl-d."
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        pass


"time"


def date(daystr):
    "return date from string."
    daystr = daystr.encode('utf-8', 'replace').decode("utf-8")
    res = time.time()
    for fmat in TIMES:
        try:
            res = time.mktime(time.strptime(daystr, fmat))
            break
        except ValueError:
            pass
    return res


def day(daystr):
    "day part in a string."
    days = None
    month = None
    yea = None
    try:
        ymdre = re.search(r'(\d+)-(\d+)-(\d+)', daystr)
        if ymdre:
            (days, month, yea) = ymdre.groups()
    except ValueError:
        try:
            ymre = re.search(r'(\d+)-(\d+)', daystr)
            if ymre:
                (days, month) = ymre.groups()
                yea = time.strftime("%Y", time.localtime())
        except Exception as ex:
            raise NoDate(daystr) from ex
    if days:
        days = int(days)
        month = int(month)
        yea = int(yea)
        dte = f"{days} {MONTH[month]} {yea}"
        return time.mktime(time.strptime(dte, r"%d %b %Y"))
    raise NoDate(daystr)


def elapsed(seconds, short=True):
    "seconds to string."
    txt = ""
    nsec = float(seconds)
    if nsec < 1:
        return f"{nsec:.2f}s"
    yea     = 365 * 24 * 60 * 60
    week    = 7 * 24 * 60 * 60
    nday    = 24 * 60 * 60
    hou    = 60 * 60
    minute  = 60
    yeas    = int(nsec / yea)
    nsec   -= yeas * yea
    weeks   = int(nsec / week)
    nsec   -= weeks * week
    nrdays  = int(nsec / nday)
    nsec   -= nrdays * nday
    hours   = int(nsec / hou)
    nsec   -= hours * hou
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


def extract(daystr):
    "extract date/time from string."
    previous = ""
    line = ""
    daystr = str(daystr)
    res = None
    for word in daystr.split():
        line = previous + " " + word
        previous = word
        try:
            res = date(line.strip())
            break
        except ValueError:
            res = None
        line = ""
    return res


def fntime(daystr):
    "return time from path."
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


def hour(daystr):
    "return hour in string."
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


def timed(txt):
    "scan string for date/time."
    try:
        target = day(txt)
    except NoDate:
        target = extract(today())
    hours = hour(txt)
    if hours:
        target += hours
    return target


def parsetxt(txt):
    "parse text for date/time."
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
            target = day(txt)
        except NoDate:
            target = extract(today())
        hours = hour(txt)
        if hours:
            target += hours
    return target


def today():
    "return start of the day."
    return str(datetime.datetime.today()).split()[0]


def __dir__():
    return (
        'cdir',
        'date',
        'day',
        'elapsed',
        'extract',
        'fntime',
        'hour',
        'ident',
        'md5sum',
        'spl',
        'time',
        'parsetxt',
        'today',
        'where',
        'wrapped'
    )
