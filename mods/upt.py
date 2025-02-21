# This file is placed in the Public Domain.


"show uptime/version"


import time


from nixt.clients import Config
from nixt.package import STARTTIME
from nixt.utility import elapsed


def upt(event):
    event.reply(elapsed(time.time()-STARTTIME))


def ver(event):
    event.reply(f"{Config.name.upper()} {Config.version}")


def __dir__():
    return (
        'upt',
        'ver'
    )
