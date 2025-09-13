# This file is placed in the Public Domain.


"commands"


import importlib
import importlib.util
import inspect
import logging
import os
import sys
import threading
import _thread


from .methods import j, md5sum, parse, spl
from .handler import Fleet
from .runtime import launch, rlog


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
        module = importer(name)
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


def scan(module):
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in inspect.signature(cmdz).parameters:
            Commands.add(cmdz)


"modules"


def importer(name, path=None):
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
        try:
            spec = importlib.util.spec_from_file_location(name, pth)
            module = importlib.util.module_from_spec(spec)
            if module:
                sys.modules[name] = module
                spec.loader.exec_module(module)
                rlog("info", f"load {pth}")
                return module
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


def inits(names):
    modz = []
    for name in sorted(spl(names)):
        try:
            module = importer(name)
            if not module:
                continue
            if "init" in dir(module):
                thr = launch(module.init)
                modz.append((module, thr))
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()
    return modz


def modules():
    if not os.path.exists(Commands.mod):
        return {}
    return sorted([
            x[:-3] for x in os.listdir(Commands.mod)
            if x.endswith(".py") and not x.startswith("__")
           ])


def scanner(names=None):
    res = []
    for nme in sorted(modules()):
        if names and nme not in spl(names):
            continue
        module = importer(nme)
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
    tbl = importer("tbl")
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
        'importer',
        'inits',
        'modules',
        'scan',
        'scanner',
        'table'
    )
