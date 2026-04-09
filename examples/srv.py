# This file is placed in the Public Domain.


"systemd service file"


from nixt.runtime import Main


def srv(event):
    "generate systemd service file."
    import getpass
    name = getpass.getuser()
    event.reply(SYSTEMD % (Main.name.upper(), name, name, name, Main.name))


srv.skip = "irc"


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
