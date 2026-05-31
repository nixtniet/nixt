# This file is placed in the Public Domain.


"text logging"


from nixt.defines import Base, Disk


class Log(Base):

    def __init__(self):
        super().__init__()
        self.txt = ''


class Cmd:

    def add(event):
        "log text."
        if not event.rest:
            event.reply("log add <txt>")
            return
        obj = Log()
        obj.txt = event.rest
        Disk.write(obj)
        event.reply("ok")
