# This file is placed in the Public Domain.


"background daemon"


from nixt.defines import Runtime


def dae(event):
    "background script."
    Runtime.daemon(Main.verbose, Main.nochdir)
    Runtime.privileges()
    Runtime.configure(Main)
    Runtime.pidfile(Main.name)
    Runtime.scan(Main)
    Runtime.init(Main)
    Runtime.forever()
