# This file is placed in the Public Domain.


"md5sum"


from ..package import getmod
from ..utility import md5sum


def md5(event):
    tbl = getmod("tbl")
    if tbl:
        event.reply(md5sum(tbl.__file__))
    else:
        event.reply("table is not there.")
