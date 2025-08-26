# This file is placed in the Public Domain.


"find"


import time


from nixt.cache import Cache
from nixt.find  import find, fntime
from nixt.func  import fmt
from nixt.paths import types
from nixt.utils import elapsed


def fnd(event):
    if not event.rest:
        if Cache.disk:
            tps = types()
        else:
            tps = Cache.types
        res = sorted([x.split('.')[-1].lower() for x in tps])
        if res:
            event.reply(",".join(res))
        return
    clz = event.args[0]
    nmr = 0
    for fnm, obj in find(clz, event.gets):
        event.reply(f"{nmr} {fmt(obj)} {elapsed(time.time()-fntime(fnm))}")
        nmr += 1
    if not nmr:
        event.reply("no result")
