# This file is placed in the Public Domain.


from nixt.brokers import get


def sil(event):
    bot = get(event.orig)
    bot.silent = True
    event.reply("ok")


def lou(event):
    bot = get(event.orig)
    bot.silent = False
    event.reply("ok")
