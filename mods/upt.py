# This file is placed in the Public Domain.


"uptime"


import time


from nixt.defines import Time


def upt(event):
    "show uptiome."
    event.reply(Time.elapsed(time.time()-Time.starttime))
