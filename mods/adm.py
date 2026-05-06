#  This file is placed in the Public Domain.


"administrator"


import os


from nixt.defines import Commands, Json, Main, Mods, Utils, Workdir


import nixt


j = os.path.join


def srv(event):
    "generate systemd service file."
    import getpass
    name = getpass.getuser()
    event.reply(SYSTEMD % (Main.name.upper(), name, name, name, Main.name))


def tbl(event):
    "create table."
    core = {}
    md5s = {}
    pkgname = Utils.pkgname(Commands)
    for name, module in Mods.all():
        md5s[name] = Utils.md5(module.__file__)
        Commands.scan(module)
    corepath = nixt.__spec__.loader._path._path[0]
    for path in os.listdir(corepath):
        if path.startswith("__") or not path.endswith(".py"):
            continue
        name = path[:-3]
        core[name] = Utils.md5(j(corepath, path))    
    event.reply("# This file is placed in the Public Domain.\n\n")
    event.reply('"tables"\n\n')
    event.reply(f"NAMES = {Json.dumps(Commands.names, indent=4, sort_keys=True)}\n\n")
    event.reply(f"CORE = {Json.dumps(core, indent=4, sort_keys=True)}\n\n")
    event.reply(f"MD5 = {Json.dumps(md5s, indent=4, sort_keys=True)}")


def wdr(event):
    "show working directory."
    event.reply(Workdir.workdir())


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
