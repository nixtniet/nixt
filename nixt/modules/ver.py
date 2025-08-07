# This file is placed in the Public Domain.


"version"


from .. import __version__


def ver(event):
    event.reply(str(__version__))
