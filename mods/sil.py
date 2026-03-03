# This file is placed in the Public Domain.


"silence"


from nixt.kernels import broker


def sil(event):
    bot = broker.retrieve(event.orig)
    if not bot:
        event.reply("no bot in fleet.")
        return
    bot.silent = True
    event.reply("ok")


def lou(event):
    bot = broker.retrieve(event.orig)
    if not bot:
        event.reply("no bot in fleet.")
        return
    bot.silent = False
    event.reply("ok")
