# This file is placed in the Public Domain.


"locate objects"


import time


from nixt.locater import find, fntime
from nixt.objects import fmt
from nixt.workdir import long, skel, types
from nixt.utility import elapsed


def fnd(event):
    skel()
    if not event.rest:
        res = sorted([x.split('.')[-1].lower() for x in types()])
        if res:
            event.reply(",".join(res))
        return
    otype = event.args[0]
    clz = long(otype)
    nmr = 0
    for fnm, obj in list(find(clz, event.gets)):
        event.reply(f"{nmr} {fmt(obj)} {elapsed(time.time()-fntime(fnm))}")
        nmr += 1
    if not nmr:
        event.reply("no result")


def __dir__():
    return (
        'fnd',
    )
