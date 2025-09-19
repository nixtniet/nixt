# This file is placed in the Public Domain.


"scripts"


import sys
import termios


from .brokers import Fleet
from .command import table
from .daemons import daemon, inits, pidfile, privileges
from .methods import parse
from .objects import update
from .package import Mods
from .threads import level
from .workdir import Workdir, pidname, setwd


NAME = Workdir.name


class Config:

    debug = False
    default = "irc,mdl,rss"
    gets = {}
    init  = ""
    level = "warn"
    mod = ""
    opts = ""
    otxt = ""
    sets = {}
    verbose = False
    version = 432
    wdr = ""


def background():
    daemon("-v" in sys.argv)
    privileges()
    boot(False)
    pidfile(pidname(NAME))
    inits(Config.init or Config.default)
    forever()


def console():
    import readline # noqa: F401
    boot()
    for _mod, thr in inits(Config.init):
        if "w" in Config.opts:
            thr.join(30.0)
    csl = Console()
    csl.start(daemon=True)
    forever()


def control():
    if len(sys.argv) == 1:
        return
    boot()
    Commands.add(md5)
    Commands.add(srv)
    Commands.add(tbl)
    csl = CLI()
    evt = Event()
    evt.orig = repr(csl)
    evt.type = "command"
    evt.txt = Config.otxt
    command(evt)
    evt.wait()


def service():
    privileges()
    boot(False)
    pidfile(pidname(NAME))
    inits(Config.init or Config.default)
    forever()


def boot(doparse=True):
    if doparse:
        parse(Config, " ".join(sys.argv[1:]))
        update(Config, Config.sets, empty=False)
        Mods.mod = Config.mod
        Workdir.wdr = Config.wdr
    level(Config.level)
    if "v" in Config.opts:
        banner()
    if 'e' in Config.opts:
        pkg = sys.modules.get(NAME)
        pth = pkg.__path__[0]
        pth = os.sep.join(pth.split(os.sep)[:-4])
        pth = os.path.join(pth, 'share', NAME,  'examples')
        Mods.mod = Config.mod = pth
        Mods.package = "mods"
    if "m" in Config.opts:
        Mods.mod = Config.mod = "mods"
        Mods.package = "mods"
    if "a" in Config.opts:
        Config.init = ",".join(modules())
    setwd(NAME)
    table(CHECKSUM)
    Commands.add(cmd)
    Commands.add(ver)
    logging.info("workdir is %s", Workdir.wdr)


def check(txt):
    args = sys.argv[1:]
    for arg in args:
        if not arg.startswith("-"):
            continue
        for char in txt:
            if char in arg:
                return True
    return False


def wrapped(func):
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        out("")
    Fleet.shutdown()


def wrap(func):
    import termios
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        wrapped(func)
    finally:
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def main():
    if check("c"):
        wrap(console)
    elif check("d"):
        background()
    elif check("s"):
        wrapped(service)
    else:
        wrapped(control)


def __dir__():
    return (
        'NAME',
        'background',
        'boot',
        'wrapped',
        'console',
        'constrol',
        'serivce',
        'wrap',
        'main'
    )
