# This file is placed in the Public Domain.


"show path to website"


from nixt.defines import d, e, j


whitelist = ['path']


def path(event):
    pth = d(d(__file__))
    pth = j(pth, "network", "index.html")
    if e(pth):
        event.reply(f"file://{pth}")
    else:
        event.reply("no index.html")
