# This file is placed in the Public Domain.


"commands"


import inspect
import os
import sys
import threading


from nixt.methods import importer, j, md5sum, parse, rlog, spl
from nixt.handler import Fleet


lock = threading.RLock()


class Commands:

    cmds = {}
    debug = False
    md5s = {}
    mod = j(os.path.dirname(__file__), "modules")
    names = {}

    @staticmethod
    def add(func) -> None:
        name = func.__name__
        modname = func.__module__.split(".")[-1]
        Commands.cmds[name] = func
        Commands.names[name] = modname

    @staticmethod
    def get(cmd):
        func = Commands.cmds.get(cmd, None)
        if func:
            return func
        name = Commands.names.get(cmd, None)
        if not name:
            return
        module = getmod(name)
        if not module:
            return
        scan(module)
        if Commands.debug:
            module.DEBUG = True
        return Commands.cmds.get(cmd, None)


def command(evt):
    parse(evt)
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        Fleet.display(evt)
    evt.ready()


def getmod(name, path=None):
    with lock:
        module = sys.modules.get(name, None)
        if module:
            return module
        if not path:
            path = Commands.mod
        pth = j(path, f"{name}.py")
        if not os.path.exists(pth):
            return
        if name != "tbl" and md5sum(pth) != Commands.md5s.get(name, None):
            rlog("warn", f"md5 error on {pth.split(os.sep)[-1]}")
        return importer(name, pth) 


def modules():
    if not os.path.exists(Commands.mod):
        return {}
    return sorted([
            x[:-3] for x in os.listdir(Commands.mod)
            if x.endswith(".py") and not x.startswith("__")
           ])


def scan(module):
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in inspect.signature(cmdz).parameters:
            Commands.add(cmdz)


def scanner(names=None):
    res = []
    for nme in sorted(modules()):
        if names and nme not in spl(names):
            continue
        module = getmod(nme)
        if not module:
            continue
        scan(module)
        res.append(module)
    return res


def table(checksum=""):
    pth = j(Commands.mod, "tbl.py")
    if os.path.exists(pth):
        if checksum and md5sum(pth) != checksum:
            rlog("warn", "table checksum error.")
    tbl = getmod("tbl")
    if tbl:
        if "NAMES" in dir(tbl):
            Commands.names.update(tbl.NAMES)
        if "MD5" in dir(tbl):
            Commands.md5s.update(tbl.MD5)
    else:
        scanner()


"interface"


def __dir__():
    return (
        'Commands',
        'command',
        'getmod',
        'modules',
        'scan',
        'scanner',
        'table'
    )
