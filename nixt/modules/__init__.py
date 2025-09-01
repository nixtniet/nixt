# This file is placed in the Public Domain.


"modules"


from ..pkg import modules


class Main:

    debug    = False
    gets     = {}
    init     = ""
    level    = "warn"
    md5      = True
    name     = __package__.split(".", maxsplit=1)[0].lower()
    opts     = {}
    otxt     = ""
    sets     = {}
    verbose  = False
    version  = 401


def __dir__():
    return modules()
