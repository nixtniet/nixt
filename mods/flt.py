# This file is placed in the Public Domain.


"show bot in fleet"


from nixt.brokers import broker
from nixt.objects import fqn


def flt(event):
    clts = list(broker.objs("announce"))
    if not clts:
        event.reply("no bots")
        return
    if event.args:
        index = int(event.args[0])
        if index < len(clts):
            event.reply(str(clts[index]))
        else:
            event.reply("no matching client in fleet.")
        return
    event.reply(' | '.join([fqn(o).split(".")[-1] for o in clts]))
