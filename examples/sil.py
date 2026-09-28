# This file is placed in the Public Domain.


"silence"


from nixt.defines import Broker


def lou(message):
    "disable silent mode."
    bot = Broker.get(message.orig)
    if not bot:
        message.reply("no bot in fleet.")
        return
    bot.silent = False
    message.ok()


def sil(message):
    "enable silent mode."
    bot = Broker.get(message.orig)
    if not bot:
        message.reply("no bot in fleet.")
        return
    bot.silent = True
    message.ok()
