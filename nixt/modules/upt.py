# This file is placed in the Public Domain.


"uptime"


import time


from ..run import STARTTIME, elapsed


def upt(event):
    event.reply(elapsed(time.time()-STARTTIME))
