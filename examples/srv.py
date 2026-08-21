# This file is placed in the Public Domain.


"create systemd service file"


from nixt.defines import Main


def srv(event):
    "generate systemd service file."
    if not Main.sets.admin:
        event.reply("creating service files needs --admin")
        return
    import getpass
    name = getpass.getuser()
    event.reply(SYSTEMD % (
                           Main.name.upper(),
                           name,
                           name,
                           name,
                           Main.name
                          ))


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
