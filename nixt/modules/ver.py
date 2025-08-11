# This file is placed in the Public Domain.


"version"


from ..run import Main


def ver(event):
    event.reply(str(Main.version))
