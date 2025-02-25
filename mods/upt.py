# This file is placed in the Public Domain.


"uptime"


import time


from nixt.find    import elapsed
from nixt.reactor import STARTTIME


def upt(event):
    event.reply(elapsed(time.time()-STARTTIME))
