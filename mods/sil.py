# This file is placed in the Public Domain.
# pylint: disable=C0116


"silence"


from nixt.runtime import broker


def sil(event):
    bot = broker.get(event.orig)
    if not bot:
        event.reply("no bot in fleet.")
        return
    bot.silent = True
    event.reply("ok")


def lou(event):
    bot = broker.get(event.orig)
    if not bot:
        event.reply("no bot in fleet.")
        return
    bot.silent = False
    event.reply("ok")
