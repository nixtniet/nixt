# This file is placed in the Public Domain.


"kernels"


import logging
import os
import time


from .brokers import Broker
from .command import Commands
from .handler import Message
from .methods import merge, parse
from .objects import Default, update, values
from .package import Mods
from .persist import Persist
from .threads import launch
from .utility import pkgname


"defines"


broker = Broker()
cmds = Commands()
db = Persist()
mods = Mods()


"config"


class Config(Default):

    debug = False
    default = "irc,mdl,rss,wsd"
    ignore = "man,rst,udp,web"
    level = "info"
    local = True
    mods = ""
    name = pkgname(Default)
    version = 455
    wdr = os.path.expanduser(f"~/.{name}")


Cfg = Config()


"logging"


class Format(logging.Formatter):

    def format(self, record):
        record.module = record.module.upper()
        return logging.Formatter.format(self, record)


class Log:

    datefmt = "%H:%M:%S"
    format = "%(module).3s %(message)s"


def level(loglevel):
    "set log level."
    formatter = Format(Log.format, Log.datefmt)
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    logging.basicConfig(
        level=loglevel.upper(),
        handlers=[stream,],
        force=True
    )


"utilities"


def boot(args, *modlist):
    "in the beginning."
    parse(Cfg, args.txt)
    update(Cfg, Cfg.sets)
    merge(Cfg, vars(args))
    db.setwd(Cfg.wdr)
    level(Cfg.level or "info")
    if Cfg.noignore:
        Cfg.ignore = ""
    if Cfg.wdr:
        mods.dir("modules", os.path.join(Cfg.wdr, "mods"))
    for mod in modlist:
        mods.dir(mod.__name__, mod.__path__[0])
    if Cfg.local:
        mods.dir('mods', 'mods')
    if Cfg.all:
        Cfg.mods = mods.list(Cfg.ignore)


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
        bot = broker.retrieve(evt.orig)
        if bot:
            bot.display(evt)
    evt.ready()


def daemon(verbose=False, nochdir=False):
    "run in the background."
    import sys
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
    if not nochdir:
        os.chdir("/")
    os.nice(10)


def forever():
    "run forever until ctrl-c."
    while True:
        try:
            time.sleep(0.1)
        except (KeyboardInterrupt, EOFError):
            break


def init(default=True):
    "scan named modules for commands."
    thrs = []
    if default:
        defs = Cfg.default
    else:
        defs = ""
    for name, mod in mods.iter(
                               Cfg.mods or defs,
                               Cfg.ignore,
                              ):
        if "init" in dir(mod):
            thrs.append((name, launch(mod.init)))
    if Cfg.wait:
        for name, thr in thrs:
            thr.join()


def privileges():
    "drop privileges."
    import getpass
    import pwd
    pwnam2 = pwd.getpwnam(getpass.getuser())
    os.setgid(pwnam2.pw_gid)
    os.setuid(pwnam2.pw_uid)


def scanner(default=True):
    "scan named modules for commands."
    res = []
    if default:
        defs = Cfg.default
    else:
        defs = ""
    for name, mod in mods.iter(
                               Cfg.mods or defs or mods.list(),
                               Cfg.ignore,
                              ):
        cmds.scan(mod)
        if "configure" in dir(mod):
            mod.configure()
        res.append((name, mod))
    return res


def shutdown():
    "call shutdown on modules."
    logging.debug("shutdown")
    for mod in values(mods.modules):
        if "shutdown" in dir(mod):
            try:
                mod.shutdown()
            except Exception as ex:
                logging.exception(ex)


def wrap(func, *args):
    "restore console."
    import sys
    import termios
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func(*args)
    except (KeyboardInterrupt, EOFError):
        pass
    except Exception as ex:
        logging.exception(ex)
    if old:
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


"interface"


def __dir__():
    return (
        'Cfg',
        'boot',
        'broker',
        'cmds',
        'cmnd',
        'command',
        'daemon'
        'db',
        'init',
        'mods',
        'privileges',
        'scanner',
        'shutdown',
        'wrap'
    )
