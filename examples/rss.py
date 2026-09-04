# This file is placed in the Public Domain.


"rich site syndicate"


import gc
import logging
import os
import pathlib
import queue
import re
import threading
import _thread


from nixt.defines import Clients, Disk, Fetcher, Format, JSONL, Locater
from nixt.defines import Logging, Main, MD5, Method, Object, Repeater
from nixt.defines import Thread, Utils, Watcher, Workdir


logger = logging.getLogger("rss")
watcher = Watcher()


j = os.path.join


class Config(Object):

    "rss config"

    polltime = 300
    save = False


def init():
    "initialize rss module."
    Disk.read(Config, "rss", "config")
    Run.start()
    nrs = Locater.count("rss")
    txt = f"{nrs} feeds index {State.index}"
    if nrs == 1:
        txt = txt[:-1]
    logging.info(txt)


def shutdown():
    "shutdown rss module."
    Run.stop()


class Rss(Object):

    "rss item"

    def __init__(self):
        super().__init__()
        self.display_list = "title,link,author"
        self.insertid = None
        self.name = ""
        self.rss = ""


class State(Object):

    "module state"

    index = 0


class Locks:

    "locks"

    fetchlock = _thread.allocate_lock()
    importlock = _thread.allocate_lock()


class Run:

    "runtime"

    path = ""
    file = None
    lock = threading.RLock()
    matching = []
    configfn = ""
    modifiedfn = ""
    statefn = ""
    index = 0

    @classmethod
    def callback(cls):
        with cls.lock:
            cls.file.seek(State.index, 0)
            while True:
                line = cls.file.readline()
                if not line:
                    break
                Clients.announce(cls.display(JSONL.loads(line.strip())))
            State.index = cls.file.tell()
        Disk.write(State, cls.statefn)
        gc.collect(0)

    @classmethod
    def display(cls, obj, name=None):
        "display feed."
        displaylist = ""
        if name in obj:
            result = f"[{obj.name}] "
        else:
            result = ""
        try:
            displaylist = Method.get(obj, "display_list") or "title,link"
        except AttributeError:
            displaylist = "title,link,author"
        for key in displaylist.split(","):
            if not key:
                continue
            data = Method.get(obj, key, None)
            if not data:
                continue
            stripped = Utils.striphtml(data.replace("\n", " ").rstrip())
            result += Utils.unescape(stripped)
            result += " - "
        return result[:-2].rstrip()

    @classmethod
    def enable(cls, path):
        "enabke module logger."
        formatter = Format(Logging.formats, Logging.datefmt)
        filehandler = logging.handlers.TimedRotatingFileHandler(path, 'midnight')
        filehandler.setFormatter(formatter)
        if logger.handlers:
            for handler in logger.handlers:
                logger.removeHandler(handler)
        logger.addHandler(filehandler)
        logger.propagate = False
        logger.setLevel("DEBUG")

    @classmethod
    def log(cls, txt):
        "log to file."
        md5 = MD5.source(txt)[:7]
        if md5 in cls.matching:
            return
        cls.matching.append(md5)
        logger.debug(txt)

    @classmethod
    def run(cls, silent=False):
        "do a fetch run of all feeds."
        nrs = 0
        for fnm, feed in Locater.find(Method.fqn(Rss)):
            if feed.skip:
                continue
            Runners.put(fnm, feed, silent)
            nrs += 1
        return nrs

    @classmethod
    def start(cls, once=False):
        "initialise module."
        if Config.save:
            cls.path = j(Workdir.logdir("rss"), 'rss.log')
            Utils.cdir(cls.path)
            pathlib.Path(cls.path).touch()
            cls.file = open(cls.path, "a+", encoding="utf-8")
            cls.enable(cls.path)
            watcher.add(cls.path, cls.callback)
            watcher.start()
        cls.statefn = Locater.last(State) or Disk.ident(State)
        if not once:
            Repeater.add(Config.polltime, cls.run)
        
    @classmethod
    def stop(cls):
        "shutdown."
        watcher.stop()

    @classmethod
    def sync(cls):
        "sync state to disk."
        if cls.index > State.index:
            State.index = cls.index
            Disk.write(State, cls.statefn)


class Runner:

    "feed fetcher"

    def __init__(self):
        self.dosave = True
        self.queue = queue.Queue()
        self.running = threading.Event()
        self.todo = queue.Queue()

    def fetch(self, fnm, feed, silent=False):
        "fetch a feed."
        counter = 0
        for obj in self.getfeed(fnm, feed, feed.display_list):
            if obj is None:
                continue
            if Method.isempty(obj):
                continue
            fed = Object()
            Method.update(fed, obj)
            Method.update(fed, feed)
            if Config.save:
                Run.log(JSONL.logtxt(fed))
            else:
                Clients.announce(Run.display(fed))
            counter += 1
        Run.sync()
        return counter

    def getfeed(self, fnm, feed, items):
        "fetch a feed."
        result = [None,]
        response = Fetcher.geturl(feed.rss)
        if response.error or not response.data:
            logging.debug("skip %s", feed.rss)
            return result
        if "link" not in items:
            items += ",link"
        yield from RSS.parse(
                             str(response.data, "utf-8", errors='ignore'),
                             (feed.rss.endswith("atom") and "entry") or "item",
                             items
                            ) or []

    def loop(self):
        "loop to handle fetch jobs."
        while self.running.is_set():
            job = self.queue.get()
            if job is None:
                break
            self.fetch(*job)

    def put(self, *args):
        "put jobs on queue."
        self.queue.put(args)

    def start(self, daemon=True):
        "start runner."
        self.running.set()
        Thread.launch(self.loop, daemon=daemon)

    def stop(self):
        "stop runner."
        self.running.clear()
        self.queue.put(None)


class Runners:

    "pool of runners"

    runners = {}
    max = os.cpu_count()
    nrcpu = 1
    nrlast = 0

    @classmethod
    def add(cls, client):
        "add a runner."
        cls.runners[repr(client)] = client

    @classmethod
    def get(cls, orig):
        "return client by origin."
        return cls.runners.get(orig)

    @classmethod
    def init(cls, nr):
        "initialze a number of runners."
        for x in range(nr):
            runner = Runner()
            runner.start()
            cls.add(runner)

    @classmethod
    def put(cls, *args):
        "push job to a runner."
        if not cls.runners:
            cls.init(1)
        if cls.nrlast > cls.nrcpu-1:
            cls.nrlast = 0
        clt = list(cls.runners.values())[cls.nrlast]
        clt.put(*args)
        cls.nrlast += 1


class RSS:

    "RSS parser"

    @classmethod
    def getitem(cls, line, item):
        "return item from line."
        lne = ""
        index1 = line.find(f"<{item}>")
        if index1 == -1:
            return lne
        index1 += len(item) + 2
        index2 = line.find(f"</{item}>", index1)
        if index2 == -1:
            return lne
        return Utils.cdata(line[index1:index2]).strip()

    @classmethod
    def getitems(cls, text, token, nrs=None):
        "get items from text."
        index = 0
        end = len(text)
        stop = False
        nrx = -1
        while not stop:
            nrx += 1
            if nrs and nrx >= nrs:
                break
            index1 = text.rfind(f"<{token}", index, end)
            if index1 == -1:
                break
            end = index1
            index1 += len(token) + 2
            index2 = text.rfind(f"</{token}>", index1)
            if index2 == -1:
                break
            yield text[index1:index2]

    @classmethod
    def parse(cls, txt, toke="item", items="title,link"):
        "parse feed."
        for line in cls.getitems(txt, toke):
            line = line.strip()
            obj = {}
            for itm in Utils.spl(items):
                val = cls.getitem(line, itm)
                if val:
                    escaped = Utils.unescape(val.strip())
                    obj[itm] = Utils.striphtml(escaped).replace("\n", "")
            yield obj


def atr(event):
    "show attributes of a feed."
    if not event.rest:
        event.iface("<stringinurl>")
        return
    for _fnm, obj in Locater.find(Method.fqn(Rss), {'rss': event.rest}):
        request = None
        try:
            request = Fetcher.geturl(obj.rss, True)
        except Exception as ex:
            event.reply(str(ex))
            return
        if not request:
            continue
        if obj.rss.endswith('atom'):
            result = list(RSS.getitems(
                                       str(request.data, 'utf-8', errors='ignore'),
                                       'entry',
                                       1
                                      ))
        else:
            result = list(RSS.getitems(
                                       str(request.data, 'utf-8', errors='ignore'),
                                       'item',
                                       1
                                      ))
        resulting = []
        for x in re.findall('<.*?>', result[0]):
            if x[1] == '/' and len(x) > 4:
                resulting.append(x[2:-1])
        event.reply(','.join(resulting))


def dpl(event):
    "set feed items to display."
    if len(event.args) < 2:
        event.iface("<stringinurl> <item1,item2>")
        return
    setter = {"display_list": event.args[1]}
    for fnm, feed in Locater.find(Method.fqn(Rss), {"rss": event.args[0]}):
        if feed:
            Method.update(feed, setter)
            Disk.write(feed, fnm)
    event.ok()


def nme(event):
    "set name of a feed."
    if len(event.args) == 1:
        name = ""
    elif len(event.args) == 2:
        name = event.args[1]
    else:
        event.iface("<stringinurl> <name>")
        return
    selector = {"rss": event.args[0]}
    for fnm, fed in Locater.find(
                                Method.fqn(Rss),
                                selector
                               ):
        feed = Rss()
        Method.update(feed, fed)
        if feed:
            feed.name = name
            Disk.write(feed, fnm)
    event.ok()


def rem(event):
    "remove a feed."
    if len(event.args) != 1:
        event.iface("<stringinurl>")
        return
    for fnm, fed in Locater.find(Method.fqn(Rss)):
        feed = Rss()
        Method.update(feed, fed)
        if event.args[0] not in feed.rss:
            continue
        if feed:
            feed.__deleted__ = True
            Disk.write(feed, fnm)
            event.ok()
            break


def res(event):
    "restore a feed."
    if len(event.args) != 1:
        event.iface("<stringinurl>")
        return
    nrs = 0
    for fnm, fed in Locater.find(
                                Method.fqn(Rss),
                                removed=True
                               ):
        feed = Rss()
        Method.update(feed, fed)
        if event.args[0] not in feed.rss:
            continue
        nrs += 1
        feed.__deleted__ = False
        Disk.write(feed, fnm)
    event.reply(f"{nrs} feeds restored.")


def rss(event):
    "add a feed."
    if not event.rest:
        event.iface("<url>")
        return
    url = event.args[0]
    if "http://" not in url and "https://" not in url:
        event.reply("i need an url")
        return
    for fnm, result in Locater.find(
                                   Method.fqn(Rss),
                                   {"rss": url}
                                  ):
        if result:
            event.reply(f"{url} is known")
            return
    feed = Rss()
    feed.rss = event.args[0]
    Disk.write(feed)
    event.ok()


def syn(event):
    "synchronize a feed."
    if Main.debug:
        return
    nrs = Run.run(True)
    event.reply(f"{nrs} feeds synced")
