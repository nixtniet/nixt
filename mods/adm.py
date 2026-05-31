# This file is placed in the Public Domain.


"administrator"


import inspect
import os
import time


from nixt.defines import Boot, Broker, Commands, Json, Main, Md5, Mods, Object
from nixt.defines import Time, Workdir, d, j


class Cmd:

    @staticmethod
    def fleet(event):
        "list of running clients."
        try:
            index = int(event.args[0])
        except (IndexError, ValueError):
            index = None
        clts = list(Broker.objs("announce"))
        if not clts:
            event.reply("no clients")
            return
        if index is None:
            event.reply(' | '.join([Object.fqn(o).split(".")[-1] for o in clts]))
            return
        if index < len(clts):
            event.reply(str(clts[index]))
        else:
            event.reply("no matching client.")

    @staticmethod
    def service(event):
        "generate systemd service file."
        import getpass
        name = getpass.getuser()
        event.reply(SYSTEMD % (
                               Main.name.upper(),
                               name,
                               name,
                               name,
                               Main.name
                              ))

    @staticmethod
    def skel(event):
        "create directories."
        Workdir.skel()
        event.ok()

    @staticmethod
    def table(event):
        "create table."
        core = {}
        md5s = {}
        Boot.scanner()
        for name, module in Mods.modules.items():
            modname = module.__name__.split(".")[-1]
            md5s[modname] = Md5.md5(module.__file__)
            Commands.scan(module)
        corepath = d(inspect.getsourcefile(Commands))
        for path in os.listdir(corepath):
            if path.startswith("__") or not path.endswith(".py") or "statics" in path:
                continue
            name = path[:-3]
            core[name] = Md5.md5(j(corepath, path))
        event.reply("# This file is placed in the Public Domain.")
        event.reply("\n")
        event.reply('"static tables"')
        event.reply("\n")
        event.reply(f"CORE = {Json.dumps(core, indent=4, sort_keys=True)}")
        if Main.admin:
            event.reply("\n")
            event.reply(f"MODULES = {Json.dumps(md5s, indent=4, sort_keys=True)}")

    @staticmethod
    def uptime(event):
        "show uptiome."
        event.reply(Time.elapsed(time.time()-Time.starttime))

    @staticmethod
    def version(event):
        "show verson."
        event.reply(f"{Main.name.upper()}")

    @staticmethod
    def wdr(event):
        "show working directory."
        event.reply(Workdir.wdr)


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
