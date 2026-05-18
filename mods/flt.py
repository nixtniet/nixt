# This file is placed in the Public Domain.


"show running clients"


from nixt.defines import Broker, Object


def flt(event):
    try:
        index = int(event.args[0])
    except (IndexError, ValueError):
        index = None
    clts = list(Broker.objs("announce"))
    if not clts:
        event.reply("no clients")
        return
    if index is None:
        event.reply(' | '.join([Object.fqn(o).split(".")[-1] for o in clts]))
        return
    if index < len(clts):
        event.reply(str(clts[index]))
    else:
        event.reply("no matching client.")
