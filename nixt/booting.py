# This file is placed in the Public Domain.


"main program"


import os
import sys


from .command import Commands
from .configs import Main
from .defines import StaticMethod
from .handler import Console, Message
from .objects import Dict, Methods
from .package import Mods
from .persist import Disk, Locate, Workdir
from .runtime import Runtime
from .utility import Utils


from . import modules as MODS


Main.default = "irc,mdl,rss,wsd"
Main.ignore = "man,rst,udp,web"
Main.version = 8
Main.wdr = os.path.expanduser(f"~/.{Main.name}")


class Line(Console):

    def __init__(self):
        super().__init__()
        self.register("command", Commands.command)

    def raw(self, text):
        "write to console."
        Runtime.out(text)


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


class Scripts(StaticMethod):

    def background(args):
        "background script."
        Runtime.daemon(Main.verbose, Main.nochdir)
        Runtime.privileges()
        Runtime.boot(args, MODS)
        Workdir.pidfile(Main.name)
        Runtime.scanner(Main)
        Runtime.init(Main)
        Utils.forever()

    def console(args):
        "console script."
        import readline
        readline.redisplay()
        Runtime.boot(args, MODS)
        Runtime.scanner(Main, False)
        Runtime.init(Main, default=False)
        csl = CSL()
        csl.start()
        Utils.forever()

    def control(args):
        "cli script."
        if len(sys.argv) == 1:
            return
        Runtime.boot(args,MODS)
        Main.mods = Mods.list(Main.ignore)
        Runtime.scanner(Main)
        evt = Commands.cmd(Main.txt)
        for line in evt.result.values():
            Runtime.out(line)

    def service(args):
        "service script."
        Runtime.privileges()
        Runtime.banner()
        Runtime.boot(args. MODS)
        Workdir.pidfile(Main.name)
        Runtime.scanner(Main)
        Runtime.init(Main)
        Utils.forever()


class Cmd(StaticMethod):

    def cfg(event):
        if not event.args:
            event.reply(f"cfg <{Mods.has('Config') or 'modulename'}>")
            return
        name = event.args[0]
        mod = Mods.get(name)
        if not mod:
            event.reply(f"no {name} module found.")
            return
        cfg = getattr(mod, "Config", None)
        if not cfg:
            event.reply("no configuration found.")
            return
        fnm = Locate.first(cfg) or Methods.ident(cfg)
        if not event.sets:
            event.reply(
                Methods.fmt(
                    cfg,
                    Dict.keys(cfg),
                    skip=["word",]
                )
            )
            return
        Methods.edit(cfg, event.sets)
        Disk.write(Methods.skip(cfg), fnm)
        event.reply("ok")

    def cmd(event):
        "list available commands."
        event.reply(",".join(sorted(Commands.names or Commands.cmds)))

    def mod(event):
        "list available commands."
        mods = Mods.list(Main.ignore)
        if not mods:
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
    args, arguments = Runtime.getargs()
    args.txt = " ".join(arguments)
    if args.daemon:
        Commands.add(Cmd.cmd, Cmd.mod, Cmd.ver)
        Scripts.background(args)
    elif args.console:
        Commands.add(Cmd.cmd, Cmd.mod, Cmd.ver)
        Runtime.wrap(Scripts.console, args)
    elif args.service:
        Commands.add(Cmd.cmd, Cmd.mod, Cmd.ver)
        Runtime.wrap(Scripts.service, args)
    else:
        Commands.add(Cmd.cfg, Cmd.cmd, Cmd.mod, Cmd.srv, Cmd.ver)
        Runtime.wrap(Scripts.control, args)
    Runtime.shutdown()


if __name__ == "__main__":
    main()
