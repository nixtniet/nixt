# This file is placed in the Public Domain.


"todo"


from nixt.defines import Base, Disk, Locate


whitelist = ['add', 'done']


class Todo(Base):

    def __init__(self):
        super().__init__()
        self.txt = ''


def add(event):
    "add a todo."
    if not event.rest:
        event.iface("add <txt>")
        return
    obj = Todo()
    obj.txt = event.rest
    Disk.write(obj)
    event.reply("ok")


def done(event):
    "mark todo as done."
    if not event.args:
        event.iface("done <txt>")
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
