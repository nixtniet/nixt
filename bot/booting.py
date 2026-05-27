# This file is placed in the Public Domain.


"in the beginning"


import os
import pathlib
import time


from nixt.command import Commands
from nixt.message import Message
from nixt.threads import Thread
from nixt.utility import Utils, d, e, j


from .configs import Main
from .package import Mods
from .persist import Workdir


class Boot:

    md5s = {}

    @classmethod
    def check(cls):
        "check md5sums."
        if cls.md5s:
            Utils.check(d(__spec__.loader.path), cls.md5s)
        if Mods.md5s:
            Mods.check()

    @classmethod
    def core(cls):
        "calculate md5 of the statics module."
        try:
            from . import statics
        except ModuleNotFoundError:
            return ""
        return Utils.md5source(Utils.source(statics))[:7].upper()

    @classmethod
    def forever(cls):
        "run forever until ctrl-c."
        while True:
            try:
                time.sleep(0.01)
            except (KeyboardInterrupt, EOFError):
                break

    @classmethod
    def init(cls, modlist, wait=False):
        "call init of modules that have an init function."
        thrs = []
        for name in Utils.spl(modlist):
            mod = Mods.get(name)
            if not mod or "init" not in dir(mod):
                continue
            thrs.append(Thread.launch(mod.init))
        if thrs and wait:
            for thr in thrs:
                try:
                    thr.join()
                except (KeyboardInterrupt, EOFError):
                    return False
        return True

    @classmethod
    def privileges(cls):
        "drop privileges."
        import getpass
        import pwd
        pwnam2 = pwd.getpwnam(getpass.getuser())
        os.setgid(pwnam2.pw_gid)
        os.setuid(pwnam2.pw_uid)

    @classmethod
    def scanner(cls):
        "scan named modules for commands."
        for name in Utils.spl(Mods.list()):
            mod = Mods.get(name)
            if not mod:
                continue
            if "configure" in dir(mod):
                mod.configure()
            Commands.scan(mod)

    @classmethod
    def table(cls):
        "read table,"
        try:
            from .statics import CORE
            cls.md5s.update(CORE)
            return True
        except ImportError:
            return False

    @classmethod
    def writepid(cls, name):
        "write pidfile."
        filename = j(Workdir.wdr, f"{name}.pid")
        if e(filename):
            os.unlink(filename)
        path2 = pathlib.Path(filename)
        path2.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as fds:
            fds.write(str(os.getpid()))


def cmd(text):
    Workdir.wdr = os.path.expanduser(f"~/.{Main.name}")
    Mods.add(f"{Main.name}.modules", Utils.moddir())
    Mods.add("modules", Workdir.moddir())
    Log.size(len(Main.name))
    Log.level(cfg.level or "info")
    if not Commands.table():
        Boot.scanner()
    evt = Message()
    evt.kind = "command"
    evt.text = text
    Commands.command(evt)
    evt.wait()
    yield from evt.result


def __dir__():
    return (
        'Boot',
        'cmd'
    )
