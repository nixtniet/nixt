# This file is placed in the Public Domain.


"service"


from nixt.defines import Main, Runtime


def ser():
    "service script."
    Runtime.privileges()
    Runtime.configure(Main)
    Runtime.scan(Main)
    Runtime.banner()
    Runtime.pidfile(Main.name)
    Runtime.init(Main)
    Runtime.forever()
