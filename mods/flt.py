# This file is placed in the Public Domain.


"show running clients"


from nixt.face import Broker, Object


def flt(event):
    if not event.args:
        event.reply("flt [nr]")
        return
    try:
        index = int(event.args[0])
    except ValueError:
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
