# This file is placed in the Public Domain.


import queue
import threading


from .brokers import Broker
from .configs import Config
from .command import scan
from .handler import Handler
from .package import Mods, getmod
from .threads import launch
from .workdir import Workdir


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.olock = threading.RLock()
        self.oqueue = queue.Queue()
        self.silent = True
        Broker.add(self)

    def announce(self, text):
        if not self.silent:
            self.raw(text)

    def display(self, event):
        with self.olock:
            for tme in sorted(event.result):
                self.dosay(
                           event.channel,
                           event.result[tme]
                          )

    def dosay(self, channel, text):
        self.say(channel, text)

    def raw(self, text):
        raise NotImplementedError("raw")

    def say(self, channel, text):
        self.raw(text)

    def wait(self):
        self.oqueue.join()


def configure(name, version):
    Config.name = name
    Config.version = version
    Workdir.init(name)
    Mods.init(f"{name}.modules", local=True)


def scanner(names, init=False):
    mods = []
    for name in names:
        mod = getmod(name)
        if mod:
            scan(mod)
        if init and "init" in dir(mod):
            thr = launch(mod.init, Config())
            mods.append((mod, thr))
    return mods


def __dir__():
    return (
        'Client',
        'configure',
        'scanner'
   )
