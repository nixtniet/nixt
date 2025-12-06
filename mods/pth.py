# This file is placed in the Public Domain.


import os


from nixt.package import Mods


def pth(event):
    path = os.path.join(Mods.path, 'classes', "index.html")
    event.reply(f"file://{path}")
