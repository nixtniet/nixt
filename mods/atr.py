# This file is placed in the Public Domain.


"fields"


from nixt.locater import attrs


def atr(event):
    if not event.rest:
        event.reply("fld <type>")
        return
    items = attrs(event.args[0])
    if not items:
        event.reply("no fields")
    else:
        event.reply(",".join(items))
