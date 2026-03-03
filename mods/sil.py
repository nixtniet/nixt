# This file is placed in the Public Domain.


"silence"


from nixt.runtime import broker


def sil(event):
    "put bot in silent mode."
    bot = broker.get(event.orig)
    if not bot:
        event.reply("no bot in fleet.")
        return
    bot.silent = True
    event.reply("ok")


def lou(event):
    "put bot in loud mode."
    bot = broker.get(event.orig)
    if not bot:
        event.reply("no bot in fleet.")
        return
    bot.silent = False
    event.reply("ok")
