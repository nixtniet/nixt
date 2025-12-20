# This file is placed in the Public Domain.



from nixt.package import modules


def mod(event):
    event.reply(modules())
