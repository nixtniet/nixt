# This file is placed in the Public Domain.


"show uptime"


import time


from nixt.defines import Time


def upt(message):
    "show uptiome."
    message.reply(Time.elapsed(time.time()-Time.starttime))
