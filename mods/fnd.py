# This file is placed in the Public Domain.


"locate objects"


import time


from nixt.objects import fmt
from nixt.persist import find, kinds
from nixt.utility import Time


def fnd(event):
    if not event.rest:
        res = sorted([x.split('.')[-1].lower() for x in kinds()])
        if res:
            event.reply(",".join(res))
        else:
            event.reply("no data yet.")
        return
    otype = event.args[0]
    nmr = 0
    for fnm, obj in sorted(find(otype, event.gets), key=lambda x: Time.fntime(x[0])):
        event.reply(f"{nmr} {fmt(obj)} {Time.elapsed(time.time()-Time.fntime(fnm))}")
        nmr += 1
    if not nmr:
        event.reply("no result")
