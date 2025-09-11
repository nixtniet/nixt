# This file is placed in the Public Domain.


"commands"


import importlib
import importlib.util
import inspect
import logging
import os
import sys
import _thread


from .clients import Fleet
from .methods import parse
from .runtime import launch, rlog
from .utility import md5sum, j, spl


class Commands:

    cmds = {}
    debug = False
    md5s = {}
    mod = j(os.path.dirname(__file__), "modules")
    names = {}

    @staticmethod
    def add(func) -> None:
        Commands.cmds[func.__name__] = func
        Commands.names[func.__name__] = func.__module__.split(".")[-1]

    @staticmethod
    def get(cmd):
        func = Commands.cmds.get(cmd, None)
        if not func:
            name = Commands.names.get(cmd, None)
            if not name:
                return
            module = importer(name, Commands.mod)
            if module:
                scan(module)
                if Commands.debug:
                    module.DEBUG = True
                func = Commands.cmds.get(cmd)
        return func


def command(evt):
    parse(evt)
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        Fleet.display(evt)
    evt.ready()


def importer(name, path):
    module = sys.modules.get(name, None)
    if not module:
        try:
            pth = j(path, f"{name}.py")
            if not os.path.exists(pth):
                return
            if name != "tbl" and md5sum(pth) != Commands.md5s.get(name, None):
                rlog("warn", f"md5 error on {pth.split(os.sep)[-1]}")
            spec = importlib.util.spec_from_file_location(name, pth)
            module = importlib.util.module_from_spec(spec)
            if module:
                sys.modules[name] = module
                spec.loader.exec_module(module)
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()
    return module


def inits(names):
    modz = []
    for name in sorted(spl(names)):
        try:
            module = importer(name, Commands.mod)
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
        module = importer(nme, Commands.mod)
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
    tbl = importer("tbl", Commands.mod)
    if tbl:
        if "NAMES" in dir(tbl):
            Commands.names.update(tbl.NAMES)
        if "MD5" in dir(tbl):
            Commands.md5s.update(tbl.MD5)
    else:
        scanner()


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
