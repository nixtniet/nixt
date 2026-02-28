# This file is placed in the Public Domain.


"main program"


import argparse
import logging
import os
import sys
import time


from .command import cmds, cmnd, command
from .handler import Console
from .message import Message
from .methods import edit, fmt, merge, parse, skip
from .objects import keys, values, update 
from .package import mods
from .persist import Main, first, ident, pidfile, setwd, write
from .threads import launch
from .utility import forever, level


from . import modules as MODS


"config"


Main.default = "irc,mdl,rss,wsd"
Main.ignore = "man,rst,udp,web"
Main.version = 455
Main.wdr = os.path.expanduser(f"~/.{Main.name}")


"clients"


class Line(Console):

    def __init__(self):
        super().__init__()
        self.register("command", command)

    def raw(self, text):
        "write to console."
        out(text)


class CSL(Line):

    def callback(self, event):
        "wait for callback result."
        if not event.text:
            event.ready()
            return
        super().callback(event)
        event.wait()

    def poll(self):
        "poll for an event."
        evt = Message()
        evt.text = input("> ")
        evt.kind = "command"
        return evt


'runtime'

    
def banner():
    "hello."
    tme = time.ctime(time.time()).replace("  ", " ")
    print("%s %s since %s (%s)" % (
        Main.name.upper(),
        Main.version,
        tme,
        Main.level.upper(),
    ))
    sys.stdout.flush()


def boot(args):
    "in the beginning."
    parse(Main, args.txt)
    update(Main, Main.sets)
    merge(Main, vars(args))
    setwd(Main.wdr)
    level(Main.level or "info")
    if Main.noignore:
        Main.ignore = ""
    if Main.wdr:
        mods.add("modules", os.path.join(Main.wdr, "mods"))
    if MODS:
        mods.add(MODS.__name__, MODS.__path__[0])
    if Main.local:
        mods.add('mods', 'mods')
    if Main.verbose:
        banner()
    if Main.all:
        Main.mods = mods.list(Main.ignore)


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
    os.umask(0)
    if not nochdir:
        os.chdir("/")
    os.nice(10)


def getargs():
        "parse commandline arguments."
        parser = argparse.ArgumentParser(prog=Main.name, description=f"{Main.name.upper()}")
        parser.add_argument("-a", "--all", action="store_true", help="load all modules")
        parser.add_argument("-c", "--console", action="store_true", help="start console")
        parser.add_argument("-d", "--daemon", action="store_true", help="start background daemon")
        parser.add_argument("-l", "--level", default=Main.level, help='set loglevel')
        parser.add_argument("-m", "--mods", default="", help='modules to load')
        parser.add_argument("-n", "--noignore", action="store_true", help="disable ignore")
        parser.add_argument("-s", "--service", action="store_true", help="start service")
        parser.add_argument("-v", "--verbose", action='store_true',help='enable verbose')
        parser.add_argument("-w", "--wait", action='store_true',help='wait for services to start')
        parser.add_argument("--local", action="store_true", help="use local mods directory")
        parser.add_argument("--wdr", help='set working directory')
        return parser.parse_known_args()


def init(cfg, default=True):
    "scan named modules for commands."
    thrs = []
    if default:
        defs = cfg.default
    else:
        defs = ""
    for name, mod in mods.iter(cfg.mods or defs, cfg.ignore):
        if "init" in dir(mod):
            thrs.append((name, launch(mod.init)))
    if cfg.wait:
        for name, thr in thrs:
            thr.join()

def out(txt):
    print(txt.encode('utf-8', 'replace').decode("utf-8"))


def privileges():
    "drop privileges."
    import getpass
    import pwd
    pwnam2 = pwd.getpwnam(getpass.getuser())
    os.setgid(pwnam2.pw_gid)
    os.setuid(pwnam2.pw_uid)
 

def scanner(cfg, default=True):
    "scan named modules for commands."
    res = []
    if default:
       defs = cfg.default
    else:
       defs = ""
    for name, mod in mods.iter(cfg.mods or defs or mods.list(), cfg.ignore):
        cmds.scan(mod)
        if "configure" in dir(mod):
            mod.configure(cfg)
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


"scripts"


def background(args):
    "background script."
    daemon(Main.verbose, Main.nochdir)
    privileges()
    boot(args)
    pidfile(Main.name)
    scanner(Main)
    cmds.add(cmd, mod, ver)
    init(Main)
    forever()


def console(args):
    "console script."
    import readline
    readline.redisplay()
    boot(args)
    scanner(Main, False)
    cmds.add(cmd, mod, ver)
    init(Main, default=False)
    csl = CSL()
    csl.start()
    for txt in cmnd(Main.txt):
        out(txt)
    forever()


def control(args):
    "cli script."
    if len(sys.argv) == 1:
        return
    boot(args)
    Main.mods = mods.list(Main.ignore)
    scanner(Main)
    cmds.add(cfg, cmd, mod, srv, ver)
    for line in cmnd(Main.txt):
        out(line)


def service(args):
    "service script."
    privileges()
    banner()
    boot(args)
    pidfile(Main.name)
    scanner(Main)
    cmds.add(cmd, mod, ver)
    init(Main)
    forever()


"commands"


def cfg(event):
    if not event.args:
        event.reply(f"cfg <{mods.has('Config') or 'modulename'}>")
        return
    name = event.args[0]
    mod = mods.get(name)
    if not mod:
        event.reply(f"no {name} module found.")
        return
    cfg = getattr(mod, "Config", None)
    if not cfg:
        event.reply("no configuration found.")
        return
    fnm = first(cfg) or ident(cfg)
    if not event.sets:
        event.reply(
            fmt(
                cfg,
                keys(cfg),
                skip=["word",]
               )
        )
        return
    edit(cfg, event.sets)
    write(skip(cfg), fnm)
    event.reply("ok")


def cmd(event):
    "list available commands."
    event.reply(",".join(sorted(cmds.names or cmds.cmds)))


def mod(event):
    "list available commands."
    modules = mods.list(Main.ignore)
    if not modules:
        event.reply("no modules available")
        return
    event.reply(mods)


def srv(event):
    "generate systemd service file."
    import getpass
    name = getpass.getuser()
    event.reply(SYSTEMD % (Main.name.upper(), name, name, name, Main.name))


def ver(event):
    "show verson."
    event.reply(f"{Main.name.upper()} {Main.version}")


'data'


SYSTEMD = """[Unit]
Description=%s
After=multi-user.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%s -s

[Install]
WantedBy=multi-user.target"""


"main"


def main():
    "main"
    args, arguments = getargs()
    args.txt = " ".join(arguments)
    if args.daemon:
        background(args)
    elif args.console:
        wrap(console, args)
    elif args.service:
        wrap(service, args)
    else:
        wrap(control, args)
    shutdown()
