# This file is placed in the Public Domain.


"silence"


from nixt.defines import Broker


def lou(event):
    "disable silent mode."
    bot = Broker.get(event.orig)
    if not bot:
        event.reply("no bot in fleet.")
        return
    print(bot)
    bot.silent = False
    event.reply("ok")


def sil(event):
    "enable silent mode."
    bot = Broker.get(event.orig)
    if not bot:
        event.reply("no bot in fleet.")
        return
    bot.silent = True
    event.reply("ok")
