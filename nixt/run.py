# This file is placed in the Public Domain.


"runtime"


from .auto import Auto


class Main(Auto):

    debug   = False
    ignore  = 'llm,udp,web,wsd'
    init    = ""
    level   = "warn"
    md5     = False
    name    = __package__.split(".", maxsplit=1)[0].lower()
    opts    = Auto()
    verbose = False
    version = 370
