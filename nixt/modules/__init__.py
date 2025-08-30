# This file is placed in the Public Domain.


"modules"


from ..modular import modules


class Main:

    checksum = "fd204fbc5dbe4417ccc7f5d0ee9080f6"
    debug    = False
    gets     = {}
    init     = ""
    level    = "warn"
    md5      = False
    name     = __package__.split(".", maxsplit=1)[0].lower()
    opts     = {}
    otxt     = ""
    sets     = {}
    verbose  = False
    version  = 401


def __dir__():
    return modules()
