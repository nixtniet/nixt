# This file is placed in the Public Domain.


"debug"


import time


from ..client import Fleet
from ..thread import line


def dbg(event):
    event.reply("raising exception")
    raise Exception("yo!")


def brk(event):
    event.reply("borking")
    for bot in Fleet.bots.values():
        if "sock" in dir(bot):
            event.reply(f"shutdown on {bot.cfg.server}")
            time.sleep(2.0)
            try:
                bot.sock.shutdown(2)
            except OSError as ex:
                event.reply(line(ex))
