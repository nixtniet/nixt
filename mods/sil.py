# This file is placed in the Public Domain.


"silence"


from bot.defines import Broker


def sil(event):
    "enable silent mode."
    bot = Broker.get(event.orig)
    if not bot:
        event.reply("no bot in fleet.")
        return
    bot.silent = True
    event.reply("ok")


def lou(event):
    "disable silent mode."
    bot = Broker.get(event.orig)
    if not bot:
        event.reply("no bot in fleet.")
        return
    bot.silent = False
    event.reply("ok")
