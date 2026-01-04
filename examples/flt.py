# This file is placed in the Public Domain.


from nixt.brokers import objs
from nixt.threads import name


def flt(event):
    clts = list(objs("announce"))
    if event.args:
        index = int(event.args[0])
        if index < len(clts):
            event.reply(str(type((clts[index]))))
        else:
            event.reply("no matching client in fleet.")
        return
    event.reply(' | '.join([name(o) for o in clts]))
