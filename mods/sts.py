# This file is placed in the Public Domain.


"status"


from nixt.clients import Fleet
from nixt.objects import fmt


def sts(event):
    for client in Fleet.all():
        if "state" in dir(client):
            event.reply(fmt(client.state))
