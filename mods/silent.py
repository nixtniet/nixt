# This file is placed in the Public Domain.


"silence"


from nixt.defines import Broker


class Cmd:

    def off(event):
        "disable silent mode."
        bot = Broker.get(event.orig)
        if not bot:
            event.reply("no bot in fleet.")
            return
        bot.silent = False
        event.reply("ok")

    def on(event):
        "enable silent mode."
        bot = Broker.get(event.orig)
        if not bot:
            event.reply("no bot in fleet.")
            return
        bot.silent = True
        event.reply("ok")
