# This file is placed in the Public Domain.


"uptime"


import time


from ..client import STARTTIME
from ..disk   import elapsed


def upt(event):
    event.reply(elapsed(time.time()-STARTTIME))
