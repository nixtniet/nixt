# This file is placed in the Public Domain.


"todo"


from nixt.defines import Disk, Locater, Object


class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


def dne(message):
    "mark todo as done."
    if not message.args:
        message.iface("<txt>")
        return
    selector = {'txt': message.args[0]}
    nmr = 0
    for fnm, obj in Locater.find('todo', selector):
        nmr += 1
        obj.__deleted__ = True
        Disk.write(obj, fnm)
        message.ok()
        break
    if not nmr:
        message.reply("nothing todo")


def tdo(message):
    "add a todo."
    if not message.rest:
        message.iface("<txt>")
        return
    obj = Todo()
    obj.txt = message.rest
    Disk.write(obj)
    message.ok()
