# This file is placed in the Public Domain.


"locate objects"


import time


from nixt.methods import fmt
from nixt.persist import Persist
from nixt.utility import elapsed, fntime


db = Persist()

def fnd(event):
    if not event.rest:
        res = sorted([x.split('.')[-1].lower() for x in db.kinds()])
        if res:
            event.reply(",".join(res))
        else:
            event.reply("no data yet.")
        return
    otype = event.args[0]
    nmr = 0
    for fnm, obj in sorted(db.find(otype, event.gets), key=lambda x: fntime(x[0])):
        event.reply(f"{nmr} {fmt(obj)} {elapsed(time.time()-fntime(fnm))}")
        nmr += 1
    if not nmr:
        event.reply("no result")
