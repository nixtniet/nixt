# This file is placed in the Public Domain


"debug"


from ..fleet import Fleet


def dbg(event):
    event.reply("raising exception")
    raise Exception("yo!")


def brk(event):
    for bot in Fleet.bots:
        if "sock" in dir(bot):
            event.reply("shutdown on {bot.cfg.server}")
            bot.sock.shutdown(2)

v