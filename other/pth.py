# This file is placed in the Public Domain.


"path to website"


from nixt.defines import d, j


def pth(event):
    "show path to website."
    path = d(d(__file__))
    path = j(path, "network", "index.html")
    event.reply(f"file://{path}")
