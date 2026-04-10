# This file is placed in the Public Domain.


"command line interface"


from nixt.booting import Boot, Scripts


def ser(event):
    Boot.wrap(Scripts.service)
