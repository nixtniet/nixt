# This file is placed in the Public Domain.


"usefulness"


import datetime
import inspect
import logging
import os
import queue
import threading
import time
import _thread


class NoDate(Exception):

    pass


class Format(logging.Formatter):

    size = 3

    def format(self, record):
        record.module = record.module.upper()
        record.module = record.module[:Format.size]
        return logging.Formatter.format(self, record)


class Log:

    datefmt = "%H:%M:%S"
    format = "%(module)-3s %(message)s"

    @staticmethod
    def size(nr):
        "set text size."
        index = Log.format.find("-")+1
        newformat = Log.format[:index]
        newformat += str(nr)
        newformat += Log.format[index+1:]
        Log.format = newformat
        Format.size = nr

    @staticmethod
    def level(loglevel):
        "set log level."
        formatter = Format(Log.format, Log.datefmt)
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        logging.basicConfig(
            level=loglevel.upper(),
            handlers=[stream,],
            force=True
        )


class Task(threading.Thread):

    last = time.time()

    def __init__(self, func, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, None, (), daemon=daemon)
        self.event = None
        self.name = kwargs.get("name", Thread.name(func))
        self.queue = queue.Queue()
        self.result = None
        self.starttime = time.time()
        self.stopped = threading.Event()
        self.queue.put((func, args))

    def __iter__(self):
        return self

    def __next__(self):
        yield from dir(self)

    def join(self, timeout=0.0):
        "join thread and return result."
        try:
            super().join(timeout or None)
            return self.result
        except (KeyboardInterrupt, EOFError):
            if self.event and self.event.ready:
                self.event.ready()
            _thread.interrupt_main()

    def run(self):
        "run function."
        if time.time() - Task.last < 0.01:
            time.sleep(0.01)
        Task.last = time.time()
        func, args = self.queue.get()
        if args and hasattr(args[0], "ready"):
            self.event = args[0]
        try:
            self.result = func(*args)
            return self.result
        except (KeyboardInterrupt, EOFError):
            pass
        except Exception as ex:
            logging.exception(ex)
        if self.event:
            self.event.ready()
        _thread.interrupt_main()


class Thread:

    lock = threading.RLock()

    @classmethod
    def launch(cls, func, *args, **kwargs):
        "run function in a thread."
        with cls.lock:
            try:
                task = Task(func, *args, **kwargs)
                task.start()
                return task
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    @classmethod
    def name(cls, obj):
        "string of function/method."
        if inspect.ismethod(obj):
            return f"{obj.__func__.__qualname__}"
        if inspect.isfunction(obj):
            return repr(obj).split()[1]
        return repr(obj)


class Timy(threading.Timer):

    def __init__(self, sleep, func, *args, **kwargs):
        super().__init__(sleep, func)
        self.name = kwargs.get("name", Thread.name(func))
        self.sleep = sleep
        self.state = {}
        self.status = "none"
        self.state["latest"] = time.time()
        self.state["starttime"] = time.time()
        self.starttime = time.time()


class Timed:

    def __init__(self, sleep, func, *args, thrname="", **kwargs):
        self.args = args
        self.func = func
        self.kwargs = kwargs
        self.sleep = sleep
        self.name = thrname or kwargs.get("name", Thread.name(func))
        self.target = time.time() + self.sleep
        self.timer = None

    def run(self):
        "run timed function."
        self.timer.latest = time.time()
        self.timer.status = "wait"
        self.func(*self.args)
        self.timer.status = "idle"

    def start(self):
        "start timer."
        self.kwargs["name"] = self.name
        timer = Timy(self.sleep, self.run, *self.args, **self.kwargs)
        timer.start()
        self.timer = timer

    def stop(self):
        "stop timer."
        if self.timer:
            self.timer.cancel()


class Repeater(Timed):

    def run(self):
        "run function and launch timer for next run."
        Thread.launch(super().run)
        Thread.launch(self.start)


class Time:

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
    def today():
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
    def modname(obj):
        "return package name of an object."
        return obj.__module__.split(".")[-1]

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


LEVELS = {
    "notset": logging.NOTSET,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
    "fatal": logging.FATAL
}


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
        'LEVELS',
        'TIMES',
        'Log',
        'NoDate',
        'Time',
        'Utils'
    )
