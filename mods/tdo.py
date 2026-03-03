# This file is placed in the Public Domain.
# pylint: disable=,R0903


"todo"


import time



from nixt.objects import Object
from nixt.runtime import db
from nixt.utility import elapsed, fntime


class Todo(Object):

    """Todo"""

    def __init__(self):
        Object.__init__(self)
        self.txt = ''


def dne(event):
    "flag todo as done."
    if not event.args:
        event.reply("dne <txt>")
        return
    selector = {'txt': event.args[0]}
    nmr = 0
    for fnm, obj in db.find('todo', selector):
        nmr += 1
        obj.__deleted__ = True
        db.write(obj, fnm)
        event.reply("ok")
        break
    if not nmr:
        event.reply("nothing todo")


def tdo(event):
    "tdo <txt>."
    if not event.rest:
        nmr = 0
        for fnm, obj in db.find('todo', event.gets):
            lap = elapsed(time.time()-fntime(fnm))
            event.reply(f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            event.reply("no todo")
        return
    obj = Todo()
    obj.txt = event.rest
    db.write(obj)
    event.reply("ok")
