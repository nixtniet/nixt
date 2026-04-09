# This file is placed in the Public Domain.


"working directory"


from nixt.caching import Workdir


def wdr(event):
    event.reply(Workdir.workdir())
