# This file is placed in the Public Domain.


from nixt.brokers import broker


def sil(event):
    bot = broker(event.orig)
    bot.silent = True
    event.reply("ok")


def lou(event):
    bot = broker(event.orig)
    bot.silent = False
    event.reply("ok")
