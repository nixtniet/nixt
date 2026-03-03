# This file is placed in the Public Domain.


"working directory"


from nixt.runtime import db


def wdr(event):
    "show working directory."
    event.reply(db.workdir())
