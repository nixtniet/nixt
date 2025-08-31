# This file is placed in the Public Domain.


"log text"


import time


from ..objects import Object
from ..persist import Disk, Find
from ..runtime import Time

class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


def log(event):
    if not event.rest:
        nmr = 0
        for fnm, obj in Find.find('log'):
            lap = Time.elapsed(time.time() - Find.fntime(fnm))
            event.reply(f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            event.reply('no log')
        return
    obj = Log()
    obj.txt = event.rest
    Disk.write(obj)
    event.done()
