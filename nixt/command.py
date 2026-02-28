# This file is placed in the Public Domain.


"write your own commands"


import inspect


from .brokers import broker
from .message import Message
from .methods import parse
from .objects import values


class Commands:

    def  __init__(self):
        self.cmds = {}
        self.names = {}

    def add(self, *args):
        "add functions to commands."
        for func in args:
            name = func.__name__
            self.cmds[name] = func
            self.names[name] = func.__module__.split(".")[-1]

    def get(self, cmd):
        "get function for command."
        return self.cmds.get(cmd, None)

    def has(self, cmd):
        "whether cmd is registered."
        return cmd in self.cmds

    def scan(self, module):
        "scan a module for functions with event as argument."
        for key, cmdz in inspect.getmembers(module, inspect.isfunction):
            if 'event' not in inspect.signature(cmdz).parameters:
               continue
            self.add(cmdz)


cmds = Commands()


def cmnd(text):
    "parse text for command and run it."
    results = {}
    for txt in text.split(" ! "):
        evt = Message()
        evt.text = txt
        evt.type = "command"
        command(evt)
        evt.wait()
        results.update(evt.result)
    return results.values()


def command(evt):
    "command callback."
    parse(evt, evt.text)
    func = cmds.get(evt.cmd)
    if func:
        func(evt)
        bot = broker.get(evt.orig)
        if bot:
            bot.display(evt)
    evt.ready()


def __dir__():
    return (
        'cmnd',
        'cmds',
        'command'
    )
