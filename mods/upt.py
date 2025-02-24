# This file is placed in the Public Domain.


"uptime"


import time


from nixt.command import STARTTIME
from nixt.locater import elapsed


def upt(event):
    event.reply(elapsed(time.time()-STARTTIME))
