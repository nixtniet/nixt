# This file is placed in the Public Domain.


"service file"


from nixt.workdir import Workdir


NAME = Workdir.name


TXT = """[Unit]
Description=%s
After=network-online.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%s -s

[Install]
WantedBy=multi-user.target"""


def srv(event):
    import getpass
    name = getpass.getuser()
    event.reply(TXT % (NAME.upper(), name, name, name, NAME))
