# This file is placed in the Public Domain.
# pylint: disable=C0116


"show bot in fleet"


from nixt.runtime import broker
from nixt.methods import fqn


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
