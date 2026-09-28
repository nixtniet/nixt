# This file is placed in the Public Domain.


"find objects."


import time


from nixt.defines import Locater, Method, Time, Workdir


def fnd(message):
    "find objects."
    if not message.rest:
        res = sorted([x.split('.')[-1].lower() for x in Workdir.kinds()])
        if res:
            message.reply(",".join(res))
        else:
            message.reply("no data.")
        return
    otype = message.args[0]
    nmr = 0
    for fnm, obj in sorted(
                           Locater.find(otype, message.gets),
                           key=lambda x: Locater.fntime(x[0])
                          ):
        diff = time.time()-Locater.fntime(fnm)
        message.reply(f"{nmr} {Method.fmt(obj)} {Time.elapsed(diff)}")
        nmr += 1
    if not nmr:
        message.reply("no result")
