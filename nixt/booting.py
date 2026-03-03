##!/usr/bin/python3
# This file is placed in the Public Domain.
# pylint: disable=C0415

"main program"


import argparse
import sys
import time


#sys.path.insert(0, os.getcwd())


from nixt.runtime import Cfg, boot, cmds, cmnd, command, db, daemon
from nixt.runtime import forever, init, mods, privileges, scanner, shutdown
from nixt.runtime import wrap
from nixt.handler import Console, Event
from nixt.methods import edit, fmt, skipkey
from nixt.objects import keys
from nixt.persist import ident


from nixt import modules as MODS


class Line(Console):

    """Command Line Interfacce"""

    def __init__(self):
        super().__init__()
        self.register("command", command)

    def raw(self, text):
        "write to console."
        out(text)
        sys.stdout.flush()


class CSL(Line):

    """COnsole"""

    def poll(self):
        "poll for an event."
        evt = Event()
        evt.text = input("> ")
        evt.kind = "command"
        return evt


def banner():
    "hello."
    tme = time.ctime(time.time()).replace("  ", " ")
    print(f"{Cfg.name.upper()} {Cfg.version} {tme} {Cfg.level.upper()}")
    sys.stdout.flush()


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


def cfg(event):
    "configure."
    if not event.args:
        event.reply(f"cfg <{mods.has('Config') or 'modulename'}>")
        return
    name = event.args[0]
    module = mods.get(name)
    if not module:
        event.reply(f"no {name} module found.")
        return
    config = getattr(module, "Config", None)
    if not config:
        event.reply("no configuration found.")
        return
    fnm = db.first(config) or ident(config)
    if not event.sets:
        event.reply(
            fmt(
                config,
                keys(config),
                skip=["word",]
               )
        )
        return
    edit(config, event.sets)
    db.write(skipkey(config), fnm)
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


if __name__ == "__main__":
    main()
