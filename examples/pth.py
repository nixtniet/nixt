# This file is placed in the Public Domain.


import os


from nixt.configs import Config
from nixt.utility import where


def pth(event):
    path = os.path.join(where(where), "nucleus", "index.html")
    event.reply(f"file://{path}")
