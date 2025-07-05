# This file is placed in the Public Domain.


"version"


from nixt.runtime import Main


def ver(event):
    event.reply(f"{Main.name.upper()} {Main.version}")
