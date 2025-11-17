# This file is placed in the Public Domain.


"fields"


from nixt.persist import fields


def fld(event):
    if not event.rest:
        event.reply("fld <type>")
        return
    items = fields(event.args[0])
    if not items:
        event.reply("no fields")
    else:
        event.reply(".".join(items))
