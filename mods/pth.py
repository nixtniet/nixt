# This file is placed in the Public Domain.


"show path to website"




from nixt.defines import Mods
from nixt.utility import a, e, j


def pth(msg):
    "create and show path to website."
    path = j(a(Mods.moddir("numbers")), "index.html")
    if e(path):
        msg.reply(f"file://{path}")
    else:
        msg.reply("no index.html")
