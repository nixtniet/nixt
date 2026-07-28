# This file is placed in the Public Domain.


"usefulness"


import datetime
import os
import time


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


def __dir__():
    return (
        'Time',
    )
