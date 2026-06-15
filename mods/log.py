# This file is placed in the Public Domain.


"text logging"


from nixt.defines import Base, Disk


class Log(Base):

    def __init__(self):
        super().__init__()
        self.txt = ''


def log(event):
    "log text."
    if len(event.args) == 0:
        event.iface("add <txt>")
        return
    obj = Log()
    obj.txt = event.rest
    Disk.write(obj)
    event.reply("ok")
