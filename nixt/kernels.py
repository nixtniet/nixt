# This file is placed in the Public Domain.


"modules management"


import hashlib
import importlib
import logging
import os
import sys
import threading
import _thread


from .runtime import Thread


loadlock = threading.RLock()


class Main:

    checksum = "fd204fbc5dbe4417ccc7f5d0ee9080f6"
    debug    = False
    gets     = {}
    init     = ""
    level    = "warn"
    md5      = False
    name     = __package__.split(".", maxsplit=1)[0].lower()
    opts     = {}
    otxt     = ""
    sets     = {}
    verbose  = False
    version  = 401


class Kernel:

    checksum = "fd204fbc5dbe4417ccc7f5d0ee9080f6"
    loaded   = []
    md5s     = {}
    ignore   = []
    path     = os.path.dirname(__file__)
    path     = os.path.join(path, "modules")
    pname    = f"{__package__}.modules"

    @staticmethod
    def inits(names):
        modz = []
        for name in spl(names):
            try:
                module = Kernel.mod(name)
                if not module:
                    continue
                if "init" in dir(module):
                    thr = Thread.launch(module.init)
                    modz.append((module, thr))
            except Exception as ex:
                logging.exception(ex)
                _thread.interrupt_main()
        return modz

    @staticmethod
    def md5sum(path):
        with open(path, "r", encoding="utf-8") as file:
            txt = file.read().encode("utf-8")
            return hashlib.md5(txt).hexdigest()

    @staticmethod
    def mod(name, debug=False):
        with loadlock:
            module = None
            mname = f"{Kernel.pname}.{name}"
            module = sys.modules.get(mname, None)
            if not module:
                pth = os.path.join(Kernel.path, f"{name}.py")
                if not os.path.exists(pth):
                    return None
                if Kernel.md5sum(pth) == (hash or Kernel.md5s.get(name, None)):
                    logging.error(f"md5 doesn't match on {pth}")
                spec = importlib.util.spec_from_file_location(mname, pth)
                module = importlib.util.module_from_spec(spec)
                sys.modules[mname] = module
                spec.loader.exec_module(module)
                Kernel.loaded.append(module.__name__.split(".")[-1])
            if debug:
                module.DEBUG = True
            return module

    @staticmethod
    def mods(names=""):
        res = []
        for nme in sorted(Kernel.modules(Kernel.path)):
            if names and nme not in spl(names):
                continue
            module = Kernel.mod(nme)
            if not module:
                continue
            res.append(module)
        return res

    @staticmethod
    def modules(mdir=""):
        return sorted([
                x[:-3] for x in os.listdir(mdir or Kernel.path)
                if x.endswith(".py") and not x.startswith("__") and
                x[:-3] not in Kernel.ignore
               ]) 

    @staticmethod
    def sums(md5):
        pth = os.path.join(Kernel.path, "tbl.py")
        if os.path.exists(pth) and (not md5 or (Kernel.md5sum(pth) == md5)):
            try:
                module = Kernel.mod("tbl")
            except FileNotFoundError:
                return {}
            sms =  getattr(module, "MD5", None)
            if sms:
                Kernel.md5s.update(sms)
                return True
        return False


def spl(txt):
    try:
        result = txt.split(",")
    except (TypeError, ValueError):
        result = [
            txt,
        ]
    return [x for x in result if x]


def __dir__():
    return (
        'Kernel',
        'spl'
    )
