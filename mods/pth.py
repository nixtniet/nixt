# This file is placed in the Public Domain.


import os


from nixt.configs import Config
from nixt.package import Mods


def pth(event):
    path = os.path.join(Mods.path, 'nucleus', "index.html")
    event.reply(f"file://{path}")
