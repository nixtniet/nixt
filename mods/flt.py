# This file is placed in the Public Domain.


"fleet"


from nixt.clients import Fleet
from nixt.objects import fmt
from nixt.runtime import name


def flt(event):
    clts = list(Fleet.clients.values())
    try:
        event.reply(fmt(clts[int(event.args[0])]))
    except (KeyError, IndexError, ValueError):
        event.reply(",".join([name(x).split(".")[-1] for x in clts]))
