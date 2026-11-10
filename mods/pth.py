# This file is placed in the Public Domain.


"show path to website"


import os


from nixt.defines import Mods


def pth(msg):
    "create and show path to website."
    path = os.path.join(os.path.abspath(Mods.moddir("numbers")), "index.html")
    if os.path.exists(path):
        msg.reply(f"file://{path}")
    else:
        msg.reply("no index.html")
