# This file is placed in the Public Domain.


"command line interface"


from nixt.booting import Boot, Scripts
from nixt.utility import Thread


def init():
    Thread.launch(Boot.wrap, Scripts.console)
    Boot.forever()
