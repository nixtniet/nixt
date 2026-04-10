# This file is placed in the Public Domain.


"run as service"


from nixt.booting import Boot, Scripts


def ser(event):
    Boot.wrap(Scripts.service)


ser.skip = "csl,irc"
