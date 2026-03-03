# This file is placed in the Public Domain.
# pylint: disable=C0116


"working directory"


from nixt.persist import Persist


db = Persist()


def wdr(event):
    event.reply(db.workdir())
