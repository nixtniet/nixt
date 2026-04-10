# This file is placed in the Public Domain.


"command line interface"


from nixt.booting import Boot, Scripts
from nixt.utility import Thread


def csl(event):
    Thread.launch(Boot.wrap, Scripts.console)
    Boot.forever()


csl.skip = "csl,irc"
