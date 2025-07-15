# This file is placed in the Public Domain.


"version"


from nixt.command import Main


"commands"


def ver(event):
    event.reply(f"{Main.name.upper()} {Main.version}")
