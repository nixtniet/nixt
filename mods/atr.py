# This file is placed in the Public Domain.


"show attributes"


def atr(event):
    if not event.rest:
        res = sorted({x.split('.')[-1].lower() for x in db.kinds()})
        if res:
            event.reply(",".join(res))
        else:
            event.reply("no types")
        return
    itms = db.attrs(event.args[0])
    if not itms:
        event.reply("no attributes")
    else:
        event.reply(",".join(itms))
