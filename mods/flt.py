# This file is placed in the Public Domain.


from nixt.brokers import Broker
from nixt.methods import Methods
from nixt.threads import Threads


def flt(event):
    clts = Broker.all("announce")
    if event.args:
        index = int(event.args[0])
        if index < len(clts):
            event.reply(Methods.fmt(list(clts)[index]), empty=True)
        else:
            event.reply(f"only {len(clts)} clients in fleet.")
        return
    event.reply(' | '.join([Threads.name(o) for o in clts]))
