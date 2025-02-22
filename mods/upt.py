# This file is placed in the Public Domain.


"show uptime/version"


import time


from nixt.client import Config
from nixt.table  import STARTTIME
from nixt.utils  import elapsed


def upt(event):
    event.reply(elapsed(time.time()-STARTTIME))


def ver(event):
    event.reply(f"{Config.name.upper()} {Config.version}")


def __dir__():
    return (
        'upt',
        'ver'
    )
