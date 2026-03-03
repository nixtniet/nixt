# This file is placed in the Public Domain.
# pylint: disable=C0116


"show uptime"


import time


from nixt.utility import elapsed


STARTTIME = time.time()


def upt(event):
    event.reply(elapsed(time.time()-STARTTIME))
