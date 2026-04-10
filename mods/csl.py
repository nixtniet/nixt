# This file is placed in the Public Domain.


"command line interface"


from nixt.booting import Boot, Scripts


def csl(event):
    Boot.wrap(Scripts.console)
