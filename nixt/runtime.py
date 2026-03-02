##!/usr/bin/python3 
# This file is placed in the Public Domain.


"main program"


import argparse
import logging
import os
import sys
import threading
import time


#sys.path.insert(0, os.getcwd())


from nixt.brokers import Broker
from nixt.command import Commands
from nixt.handler import Console
from nixt.message import Message
from nixt.methods import edit, fmt, merge, parse, skip
from nixt.objects import Default, Object, keys, values, update 
from nixt.package import Mods, mods
from nixt.persist import Persist, ident
from nixt.threads import launch
from nixt.utility import forever, level, pkgname


from nixt import modules as MODS


"config"


class Config(Default):

    debug = False
    default = "irc,mdl,rss,wsd"
    ignore = "man,rst,udp,web"
    level = "info"
    local = True
    name = pkgname(Default)
    version = 455
    wdr = os.path.expanduser(f"~/.{name}")


broker = Broker()
cmds = Commands()
db = Persist()
Cfg = Config()


"clients"


class Line(Console):

    def __init__(self):
        super().__init__()
        self.register("command", command)
        broker.store(self)

    def raw(self, text):
        "write to console."
        out(text)
        sys.stdout.flush()


class CSL(Line):

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
        Cfg.name.upper(),
        Cfg.version,
        tme,
        Cfg.level.upper(),
    ))
    sys.stdout.flush()


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
                               {"Cfg": Cfg}
                              ):
        if "init" in dir(mod):
            thrs.append((name, launch(mod.init)))
    if Cfg.wait:
        for name, thr in thrs:
            thr.join()


def getargs():
    "parse commandline arguments."
    parser = argparse.ArgumentParser(prog=Cfg.name, description=f"{Cfg.name.upper()}")
    parser.add_argument("-a", "--all", action="store_true", help="load all modules")
    parser.add_argument("-c", "--console", action="store_true", help="start console")
    parser.add_argument("-d", "--daemon", action="store_true", help="start background daemon")
    parser.add_argument("-l", "--level", default=Cfg.level, help='set loglevel')
    parser.add_argument("-m", "--moduless", default="", help='modules to load')
    parser.add_argument("-n", "--noignore", action="store_true", help="disable ignore")
    parser.add_argument("-s", "--service", action="store_true", help="start service")
    parser.add_argument("-v", "--verbose", action='store_true',help='enable verbose')
    parser.add_argument("-w", "--wait", action='store_true',help='wait for services to start')
    parser.add_argument("--local", action="store_true", help="use local mods directory")
    parser.add_argument("--wdr", help='set working directory')
    return parser.parse_known_args()


def out(txt):
    "output text to screen."
    print(txt.encode('utf-8', 'replace').decode("utf-8"))


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
                               {"Cfg": Cfg}
                              ):
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
    daemon(Cfg.verbose, Cfg.nochdir)
    privileges()
    boot(args, MODS)
    db.pidfile(Cfg.name)
    scanner()
    cmds.add(cmd, mod, ver)
    init()
    forever()


def console(args):
    "console script."
    import readline
    readline.redisplay()
    boot(args, MODS)
    if Cfg.verbose:
        banner()
    scanner(False)
    cmds.add(cmd, mod, ver)
    init(default=False)
    csl = CSL()
    csl.start()
    for txt in cmnd(Cfg.txt):
        out(txt)
    forever()


def control(args):
    "cli script."
    if len(sys.argv) == 1:
        return
    boot(args, MODS)
    Cfg.mods = mods.list(Cfg.ignore)
    scanner()
    cmds.add(cfg, cmd, mod, srv, ver)
    for line in cmnd(Cfg.txt):
        out(line)


def service(args):
    "service script."
    privileges()
    banner()
    boot(args, MODS)
    db.pidfile(Cfg.name)
    scanner()
    cmds.add(cmd, mod, ver)
    init()
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
    fnm = db.first(cfg) or ident(cfg)
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
    db.write(skip(cfg), fnm)
    event.reply("ok")


def cmd(event):
    "list available commands."
    event.reply(",".join(sorted(cmds.names or cmds.cmds)))


def mod(event):
    "list available commands."
    modules = mods.list(Cfg.ignore)
    if not modules:
        event.reply("no modules available")
        return
    event.reply(modules)


def srv(event):
    "generate systemd service file."
    import getpass
    name = getpass.getuser()
    event.reply(SYSTEMD % (Cfg.name.upper(), name, name, name, Cfg.name))


def ver(event):
    "show verson."
    event.reply(f"{Cfg.name.upper()} {Cfg.version}")


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


#if __name__ == "__main__":
#    main()
