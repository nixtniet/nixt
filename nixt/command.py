# This file is placed in the Public Domain.


"write your own commands"


import inspect
import threading
import time


from .objects import Data, Methods
from .package import Mods
from .utility import Utils


class Event(Data):

    def __init__(self):
        Data.__init__(self)
        self._ready = threading.Event()
        self._thr = None
        self.result = {}
        self.args = []
        self.index = 0
        self.kind = "event"

    def ok(self, txt=""):
        self.reply(f"ok {txt}".strip())

    def ready(self):
        "flag message as ready."
        self._ready.set()

    def reply(self, text):
        "add text to result."
        self.result[time.time()] = text

    def wait(self, timeout=0.0):
        "wait for completion."
        self._ready.wait(timeout or None)
        if self._thr:
            self._thr.join(timeout or None)


class Commands:

    cmds = {}
    names = {}

    @classmethod
    def add(cls, *args):
        "add functions to commands."
        for func in args:
            cls.cmds[func.__name__] = func
            modname = func.__module__.split(".")[-1]
            if "__" in modname: continue
            cls.names[func.__name__] = modname

    @classmethod
    def command(cls, evt):
        "command callback."
        Methods.parse(evt, evt.text)
        func = cls.get(evt.cmd)
        if func:
            func(evt)
            if evt.client:
                evt.client.display(evt)
        evt.ready()

    @classmethod
    def commands(cls, orig):
        res = []
        for func in cls.cmds.values():
            if cls.skip(func, orig): continue
            res.append(func.__name__)
        return res

    @classmethod
    def get(cls, cmd):
        "get function for command."
        return cls.cmds.get(cmd, None)

    @classmethod
    def scan(cls, module):
        "scan a module for functions with event as argument."
        for key, cmdz in inspect.getmembers(module, inspect.isfunction):
            if 'event' in inspect.signature(cmdz).parameters:
                cls.add(cmdz)

    @classmethod
    def scanner(cls):
        "scan named modules for commands."
        for name, mod in Mods.iter(Mods.list()):
            cls.scan(mod)
            if "configure" in dir(mod):
                mod.configure()

    @classmethod
    def skip(cls, func, orig):
        if "skip" in dir(func):
            for skp in Utils.spl(func.skip):
                if skp.lower() in orig.lower(): return True
        return False


def __dir__():
    return (
        'Commands',
    )
