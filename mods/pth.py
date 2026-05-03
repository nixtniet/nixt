# This file is placed in the Public Domain.


"show path to website"


import os


d = os.path.dirname
j = os.path.join


def pth(event):
    path = d(d(__file__))
    path = j(path, "network", "index.html")
    event.reply(f"file://{path}")
