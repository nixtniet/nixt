# This file is placed in the Public Domain.


from nixt.brokers import Broker


get = Broker.get


def sil(event):
    bot = get(event.orig)
    bot.silent = True
    event.reply("ok")


def lou(event):
    bot = get(event.orig)
    bot.silent = False
    event.reply("ok")
