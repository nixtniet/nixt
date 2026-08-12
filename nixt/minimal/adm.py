# This file is placed in the Public Domain.


"administrator"


import inspect
import os


from nixt.defines import Commands, Json, Main, Mods, Md5


def srv(event):
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


def createmd5(path, data):
    for pth in os.listdir(path):
        if pth.startswith("__") or not pth.endswith(".py") or "statics" in pth:
            continue
        name = pth[:-3]
        data[name] = Md5.md5(os.path.join(path, pth))


def tbl(event):
    "create table."
    core = {}
    md5s = {}
    Mods.names = {}
    for name in Mods.list():
        module = Mods.get(name)
        md5s[name] = Md5.md5(module.__file__)
        for cmd in Commands.scan(module):
            Mods.names[cmd.__name__] = cmd.__module__.split(".")[-1]
    corepath = os.path.dirname(inspect.getsourcefile(Mods))
    createmd5(corepath, core)
    event.reply("# This file is placed in the Public Domain.")
    event.reply("\n")
    event.reply('"static tables"')
    event.reply("\n")
    event.reply(f"CORE = {Json.dumps(core, indent=4, sort_keys=True)}")
    event.reply("\n")
    event.reply(f"MODULES = {Json.dumps(md5s, indent=4, sort_keys=True)}")
    event.reply("\n")
    event.reply(f"NAMES = {Json.dumps(Mods.names, indent=4, sort_keys=True)}")


SYSTEMD = """[Unit]
Description=%s
After=multi-user.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%s --service

[Install]
WantedBy=multi-user.target"""
