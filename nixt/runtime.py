#!/usr/bin/env python3
# This file is placed in the Public Domain.


"runtime"


import os
import pathlib
import sys
import time


from .methods import parse
from .loggers import level
from .package import addpkg, getmod, modules
from .threads import launch
from .utility import spl, wrapped
from .workdir import Workdir, skel


def boot(cfg):
    "in the beginning."
    Workdir.wdr = Workdir.wdr or os.path.expanduser(f"~/.{cfg.name}")
    skel()
    parse(cfg, cfg.txt)
    level(cfg.sets.level or cfg.level or "info")


def check(text):
    "check for options."
    args = sys.argv[1:]
    for arg in args:
        if not arg.startswith("-"):
            continue
        for char in text:
               if char in arg:
                   return True
        return False


def daemon(verbose=False, nochdir=False):
    "run in the background."
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
    if not nochdir:
        os.umask(0)
        os.chdir("/")
    os.nice(10)


def forever():
    "run forever until ctrl-c."
    while True:
        try:
            time.sleep(0.1)
        except (KeyboardInterrupt, EOFError):
            break


def init(names=None, wait=False):
    "run init function of modules."
    if names is None:
        names = modules()
    mods = []
    for name in spl(names):
        module = getmod(name)
        if not module:
            continue
        if "init" in dir(module):
            thr = launch(module.init)
            mods.append((module, thr))
    if wait:
        for module, thr in mods:
            thr.join()
    return mods


def pidfile(filename):
    "write pidfile."
    if os.path.exists(filename):
        os.unlink(filename)
    path2 = pathlib.Path(filename)
    path2.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def privileges():
    "drop privileges."
    import getpass
    import pwd
    pwnam2 = pwd.getpwnam(getpass.getuser())
    os.setgid(pwnam2.pw_gid)
    os.setuid(pwnam2.pw_uid)


def wrap(func):
    "restore console."
    import termios
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        wrapped(func)
    finally:
        pass
    if old:
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def __dir__():
    return (
        'banner',
        'book',
        'check',
        'daemon',
        'forever',
        'init',
        'pidfie',
        'privileges',
        'wrap'
    )
