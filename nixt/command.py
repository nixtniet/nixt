# This file is placed in the Public Domain.


"write your own commands"


import inspect
import logging
import os
import threading


from .brokers import Fleet
from .methods import parse
from .package import Mods, getmod, modules
from .utility import md5sum, spl


DEBUG = False


j = os.path.join
lock = threading.RLock()


class Commands:

    cmds = {}
    names = {}

    @staticmethod
    def add(func):
        name  = func.__name__
        modname = func.__module__.split(".")[-1]
        Commands.cmds[name] = func
        Commands.names[name] = modname

    @staticmethod
    def get(cmd):
        func = Commands.cmds.get(cmd, None)
        if func:
            return func
        name = Commands.names.get(cmd, None)
        if name:
            module = getmod(name)
            if module:
                scan(module)
                if DEBUG:
                    module.DEBUG = True
        return Commands.cmds.get(cmd, None)


def command(evt):
    parse(evt)
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        Fleet.display(evt)
    evt.ready()


def scan(module):
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in inspect.signature(cmdz).parameters:
            Commands.add(cmdz)


def scanner(names=""):
    res = []
    logging.warning("scanning %s", Mods.mod)
    for nme in sorted(modules()):
        if names and nme not in spl(names):
            continue
        module = getmod(nme)
        if not module:
            continue
        scan(module)
        res.append(module)
    return res


def table(checksum):
    pth = j(Mods.mod, "tbl.py")
    if not os.path.exists(pth):
        logging.info("table file is not there.")
    elif checksum and md5sum(pth) != checksum:
        logging.warning("table checksum error.")
    else:
        tbl = getmod("tbl")
        if tbl:
            if "NAMES" in dir(tbl):
                Commands.names.update(tbl.NAMES)
                return
    scanner()


def __dir__():
    return (
        'Commands',
        'command',
        'scan',
        'scanner',
        'table'
    )
