# This file is placed in the Public Domain.


"show path to genocide docs"


import os


d = os.path.dirname


def pth(event):
    "create path to docs and show it."
    path = d(d(__file__))
    path = os.path.join(path, "nucleus", "index.html")
    event.reply(f"file://{path}")
