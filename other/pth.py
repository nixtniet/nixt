# This file is placed in the Public Domain.


"show path to website"


from bot.defines import d, e, j


whitelist = ['pth']


def pth(event):
    "create and show path to website."
    path = d(d(__file__))
    path = j(path, "network", "index.html")
    if e(path):
        event.reply(f"file://{path}")
    else:
        event.reply("no index.html")
