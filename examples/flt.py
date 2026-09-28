# This file is placed in the Public Domain.


"locate objects"


from nixt.defines import Broker, Method


def flt(message):
    "list of running clients."
    try:
        index = int(message.args[0])
    except (IndexError, ValueError):
        index = None
    clts = list(Broker.objs("announce"))
    if not clts:
        message.reply("no clients")
        return
    if index is None:
        message.reply(' | '.join([Method.fqn(o).split(".")[-1] for o in clts]))
        return
    if index < len(clts):
        message.reply(str(clts[index]))
    else:
        message.reply("no matching client.")
