# This file is placed in the Public Domain.


"text logging"


from nixt.defines import Disk, Object


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


def log(message):
    "log text."
    if len(message.args) == 0:
        message.iface("<txt>")
        return
    obj = Log()
    obj.txt = message.rest
    Disk.write(obj)
    message.ok()
