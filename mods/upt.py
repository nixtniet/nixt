# This file is placed in the Public Domain.


"uptime"


from nixt.utility import Time


def upt(event):
    "show uptiome."
    event.reply(Time.elapsed(time.time()-Time.starttime))
