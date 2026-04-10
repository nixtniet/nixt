# This file is placed in the Public Domain.


"background daemon"


from nixt.booting import Scripts


def dae(event):
    Scripts.background()


dae.skip = "csl,irc"
