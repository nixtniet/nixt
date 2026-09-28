# This file is placed in the Public Domain.


"show path to website"


import os


from nixt.defines import Main


a = os.path.abspath
e = os.path.exists
j = os.path.join


def pth(message):
    "create and show path to website."
    path = j(a(Main.docs), "index.html")
    if e(path):
        message.reply(f"file://{path}")
    else:
        message.reply("no index.html")
