# This file is placed in the Public Domain.


import os


from nixt.defines import Config, where


def pth(event):
    path = os.path.join(where(Config), "nucleus", "index.html")
    event.reply(f"file://{path}")
