# This file is placed in the Public Domain.


"clients"


import threading


from .object  import Object
from .reactor import Reactor


lock = threading.RLock()


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


class Client(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        self.state = Default()
        Fleet.add(self)

    def announce(self, txt) -> None:
        pass

    def raw(self, txt) -> None:
        output(txt.encode('utf-8', 'replace').decode("utf-8"))

    def say(self, channel, txt) -> None:
        self.raw(txt)


class Fleet:

    bots = {}

    @staticmethod
    def add(bot) -> None:
        Fleet.bots[repr(bot)] = bot

    @staticmethod
    def all() -> []:
        yield from Fleet.bots.values()

    @staticmethod
    def announce(txt) -> None:
        for bot in Fleet.bots.values():
            bot.announce(txt)

    @staticmethod
    def display(evt) -> None:
        with lock:
            for tme in sorted(evt.result):
                Fleet.say(evt.orig, evt.channel, evt.result[tme])
            evt.ready()

    @staticmethod
    def first() -> None:
        bots =  list(Fleet.bots.values())
        res = None
        if bots:
            res = bots[0]
        return res

    @staticmethod
    def get(orig) -> None:
        return Fleet.bots.get(orig, None)

    @staticmethod
    def say(orig, channel, txt) -> None:
        bot = Fleet.get(orig)
        if bot:
            bot.say(channel, txt)

    @staticmethod
    def wait() -> None:
        for bot in Fleet.bots.values():
            if "wait" in dir(bot):
                bot.wait()

"output"


def doprint(txt):
    print(txt.rstrip())
    sys.stdout.flush()


def output(txt):
    doprint(txt)


def nil(txt):
    pass


def enable():
    global output
    output = doprint


def disable():
    global output
    output = nil


"interface"


def __dir__():
    return (
        'Client',
        'Fleet',
        'disable',
        'enable',
        'output'
    )
