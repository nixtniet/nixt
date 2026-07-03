# This file is placed in the Public Domain.


"text logging"


from nixt.defines import Object, Disk


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


def log(event):
    "log text."
    if len(event.args) == 0:
        event.iface("<txt>")
        return
    obj = Log()
    obj.txt = event.rest
    Disk.write(obj)
    event.reply("ok")
