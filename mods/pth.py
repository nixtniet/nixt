# This file is placed in the Public Domain.


"show path to website"


from nixt.utility import d, j


def pth(event):
    path = d(d(__file__))
    path = j(path, "network", "index.html")
    event.reply(f"file://{path}")
