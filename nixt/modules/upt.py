# This file is placed in the Public Domain.


"uptime"


import time


from ..runtime import STARTTIME, Time


def upt(event):
    event.reply(Time.elapsed(time.time()-STARTTIME))
