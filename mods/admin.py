# This file is placed in the Public Domain.


"administrator"


import inspect
import os


from nixt.defines import Json, Main, Md5, Mods
from nixt.defines import d, j


whitelist = ['service', 'table']


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


def table(event):
    "create table."
    completions = []
    core = {}
    md5s = {}
    names = {}
    for name in Mods.list():
        module = Mods.get(name)
        md5s[name] = Md5.md5(module.__file__)
        for cmd in Mods.getcmds(module):
            names[cmd] = name
            completions.append(f"{name}-{cmd}")
    corepath = d(inspect.getsourcefile(Mods))
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
    event.reply("\n")
    event.reply(f"COMPLETIONS = {Json.dumps(completions, indent=4, sort_keys=True)}")
    event.reply("\n")
    event.reply(f"NAMES = {Json.dumps(names, indent=4, sort_keys=True)}")


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
