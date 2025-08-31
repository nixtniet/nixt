# This file is placed in the Public Domain.


"find"


import time


from ..objects import fmt
from ..persist import Find, Workdir
from ..runtime import Time


def fnd(event):
    Workdir.skel()
    if not event.rest:
        res = sorted([x.split('.')[-1].lower() for x in Workdir.types()])
        if res:
            event.reply(",".join(res))
        return
    otype = event.args[0]
    clz = Workdir.long(otype)
    nmr = 0
    for fnm, obj in list(Find.find(clz, event.gets)):
        event.reply(f"{nmr} {fmt(obj)} {Time.elapsed(time.time()-Find.fntime(fnm))}")
        nmr += 1
    if not nmr:
        event.reply("no result")
