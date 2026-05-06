#  This file is placed in the Public Domain.


"administrator"


from nixt.defines import Commands, Json, Main, Mods, Workdir


def srv(event):
    "generate systemd service file."
    import getpass
    name = getpass.getuser()
    event.reply(SYSTEMD % (Main.name.upper(), name, name, name, Main.name))


def tbl(event):
    "create table."
    for name, module in Mods.all():
        Commands.scan(module)
    event.reply(f"NAMES = {Json.dumps(Commands.names, indent=4, sort_keys=True)}")


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
