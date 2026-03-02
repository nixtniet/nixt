# This file is placed in the Public Domain.


"working directory"


from nixt.persist import Persist


db = Persist()


def wdr(event):
    event.reply(db.workdir())
