# This file is placed in the Public Domain.


"uptime"


import time


from nixt.run   import STARTTIME
from nixt.utils import elapsed


def upt(event):
    event.reply(elapsed(time.time()-STARTTIME))
