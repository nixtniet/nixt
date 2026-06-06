# This file is placed in the Public Domain.


"show path to website"


from nixt.defines import d, j


whitelist = ['path']


def path(event):
    pth = d(d(__file__))
    pth = j(pth, "network", "index.html")
    event.reply(f"file://{pth}")
