# This file is placed in the Public Domain.


from nixt.brokers import objs
from nixt.methods import fmt
from nixt.threads import name


def flt(event):
    clts = objs("announce")
    if event.args:
        index = int(event.args[0])
        if index < len(clts):
            event.reply(fmt(list(clts)[index]), empty=True)
        else:
            event.reply(f"only {len(clts)} clients in fleet.")
        return
    event.reply(' | '.join([name(o) for o in clts]))
