# This file is placed in the Public Domain.


"todo"


from nixt.objects import Object
from nixt.persist import Disk, Locate


class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


def dne(event):
    "mark todo as done."
    if not event.args:
        event.iface("<txt>")
        return
    selector = {'txt': event.args[0]}
    nmr = 0
    for fnm, obj in Locate.find('todo', selector):
        nmr += 1
        obj.__deleted__ = True
        Disk.write(obj, fnm)
        event.reply("ok")
        break
    if not nmr:
        event.reply("nothing todo")


def tdo(event):
    "add a todo."
    if not event.rest:
        event.iface("<txt>")
        return
    obj = Todo()
    obj.txt = event.rest
    Disk.write(obj)
    event.reply("ok")
