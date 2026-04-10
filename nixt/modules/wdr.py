# This file is placed in the Public Domain.


"working directory"


from nixt.persist import Workdir


def wdr(event):
    event.reply(Workdir.workdir())
