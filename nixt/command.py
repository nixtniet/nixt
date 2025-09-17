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


from nixt.clients import Fleet
from nixt.methods import md5sum, parse, spl
from nixt.persist import j


DEBUG = False


lock = threading.RLock()


class Commands:

    mod     = j(os.path.dirname(__file__), "modules")
    cmds    = {}
    md5s    = {}
    names   = {}
    package = __name__.split(".", maxsplit=1)[0] + "." + "modules"

    @staticmethod
    def add(func):
        name                 = func.__name__
        modname              = func.__module__.split(".")[-1]
        Commands.cmds[name]  = func
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


def getmod(name, path=None):
    with lock:
        mname = Commands.package + "." +  name
        module = sys.modules.get(mname, None)
        if module:
            return module
        if not path:
            path = Commands.mod
        pth = j(path, f"{name}.py")
        if os.path.exists(pth):
            if name != "tbl" and (Commands.md5s and md5sum(pth) != Commands.md5s.get(name, None)):
                logging.warning("md5 error on %s", pth.split(os.sep)[-1])
        return importer(mname, pth)


def importer(name, pth):
    module = None
    try:
        spec = importlib.util.spec_from_file_location(name, pth)
        if spec:
            module = importlib.util.module_from_spec(spec)
            if module:
                sys.modules[name] = module
                if spec.loader:
                    spec.loader.exec_module(module)
                logging.info("load %s", pth)
    except Exception as ex:
        logging.exception(ex)
        _thread.interrupt_main()
    return module


def modules():
    if not os.path.exists(Commands.mod):
        return {}
    return {
            x[:-3] for x in os.listdir(Commands.mod)
            if x.endswith(".py") and not x.startswith("__")
           }


def scan(module):
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in inspect.signature(cmdz).parameters:
            Commands.add(cmdz)


def scanner(names=""):
    res = []
    logging.warning("scanning %s", Commands.mod)
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
    pth = j(Commands.mod, "tbl.py")
    if not os.path.exists(pth):
        logging.info("table file is not there.")
    elif checksum and md5sum(pth) != checksum:
        logging.warning("table checksum error.")
    else:
        tbl = getmod("tbl")
        if tbl:
            if "NAMES" in dir(tbl):
                Commands.names.update(tbl.NAMES)
            if "MD5" in dir(tbl):
                Commands.md5s.update(tbl.MD5)
            return
    scanner()


def __dir__():
    return (
        'Commands',
        'command',
        'getmod',
        'importer',
        'modules',
        'scan',
        'scanner',
        'table'
    )
