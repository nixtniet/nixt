# This file is placed in the Public Domain.


"modules management"


import hashlib
import importlib
import importlib.util
import logging
import os
import pathlib
import sys
import threading
import time
import _thread


from .runtime import Thread, rlog


loadlock = threading.RLock()


class Main:

    debug    = False
    gets     = {}
    init     = ""
    level    = "warn"
    md5      = True
    name     = __package__.split(".", maxsplit=1)[0].lower()
    opts     = {}
    otxt     = ""
    sets     = {}
    verbose  = False
    version  = 401


class Kernel:

    loaded   = []
    md5s     = {}
    ignore   = []
    path     = os.path.dirname(__file__)
    path     = os.path.join(path, "modules")
    pname    = f"{__package__}.modules"

    @staticmethod
    def banner():
        if "v" in Main.opts:
            tme = time.ctime(time.time()).replace("  ", " ")
            rlog("warn", f"{Main.name.upper()} {Main.version} since {tme} ({Main.level.upper()})")
            rlog("warn", f"loaded {",".join(Kernel.modules())}")

    @staticmethod
    def daemon(verbose=False):
        pid = os.fork()
        if pid != 0:
            os._exit(0)
        os.setsid()
        pid2 = os.fork()
        if pid2 != 0:
            os._exit(0)
        if not verbose:
            with open('/dev/null', 'r', encoding="utf-8") as sis:
                os.dup2(sis.fileno(), sys.stdin.fileno())
            with open('/dev/null', 'a+', encoding="utf-8") as sos:
                os.dup2(sos.fileno(), sys.stdout.fileno())
            with open('/dev/null', 'a+', encoding="utf-8") as ses:
                os.dup2(ses.fileno(), sys.stderr.fileno())
        os.umask(0)
        os.chdir("/")
        os.nice(10)

    @staticmethod
    def forever():
        while True:
            try:
                time.sleep(0.1)
            except (KeyboardInterrupt, EOFError):
                break

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
                if name != "tbl" and Kernel.md5sum(pth) != Kernel.md5s.get(name, None):
                    rlog("warn", f"md5 error on {pth.split(os.sep)[-1]}")
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
    def pidfile(filename):
        if os.path.exists(filename):
            os.unlink(filename)
        path2 = pathlib.Path(filename)
        path2.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as fds:
            fds.write(str(os.getpid()))

    @staticmethod
    def privileges():
        import getpass
        import pwd
        pwnam2 = pwd.getpwnam(getpass.getuser())
        os.setgid(pwnam2.pw_gid)
        os.setuid(pwnam2.pw_uid)

    @staticmethod
    def sums(checksum):
        if not Main.md5:
            return True
        pth = os.path.join(Kernel.path, "tbl.py")
        if not os.path.exists(pth):
            rlog("warn", "tbl.py is missing.")
            return False        
        if checksum and Kernel.md5sum(pth) != checksum:
            rlog("warn", "table checksum error.")
            return False
        try:
            module = Kernel.mod("tbl")
        except FileNotFoundError:
            rlog("warn", "table is not there.")
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
