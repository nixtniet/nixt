# This file is placed in the Public Domain.


"in the beginning"


import inspect
import threading
import time
import _thread


from .clients import Broker, Client
from .command import Commands
from .configs import Main
from .encoder import JSON
from .objects import Methods
from .package import Mods
from .persist import Workdir
from .threads import Threads
from .utility import MD5, Event, Log, Logging, Utils, d


logger = Log(__name__)


class Boot:

    "at startup"

    core = {}
    running = Event()
    stopped = Event()

    @classmethod
    def configure(cls):
        "setup basic variables."
        Logging.configure()
        Workdir.configure()
        Mods.configure()
        MD5.core()

    @classmethod
    def forever(cls):
        "run forever until ctrl-c."
        cls.running.set()
        while cls.running.is_set():
            try:
                time.sleep(0.1)
            except (KeyboardInterrupt, EOFError):
                break
        cls.stopped.set()

    @classmethod
    def init(cls, names, wait=False):
        "call init of modules that have an init function."
        thrs = []
        for name in Utils.spl(names):
            mod = Mods.get(name)
            if not mod or "init" not in dir(mod):
                continue
            thrs.append(Threads.start(mod.init, name=f"init {name}"))
        if thrs and wait:
            for thr in thrs:
                thr.join()
        return True

    @classmethod
    def shutdown(cls, wait=True):
        "call stop on clients."
        logger.info("shutdown")
        for client in Broker.objs("wait"):
            logger.debug("wait %s", client)
            try:
                client.wait()
            except (KeyboardInterrupt, EOFError):
                pass
        time.sleep(0.01)
        for client in Broker.objs("stop"):
            logger.debug("stop %s", client)
            try:
                client.stop()
            except (KeyboardInterrupt, EOFError):
                pass
        time.sleep(0.01)
        if wait:
            while True:
                if len(threading.enumerate()) <= 1:
                    break
                time.sleep(0.01)
        cls.stopped.set()

    @classmethod
    def table(cls):
        "read table,"
        try:
            from .statics import CORE
            cls.core.update(CORE)
        except (ImportError, SyntaxError, ValueError):
            pass
        if cls.core:
            MD5.check(cls.core)

    @classmethod
    def wrapped(cls, func, *args):
        "wrap function in a try/except, silence ctrl-c/ctrl-d."
        try:
            func(*args)
        except (KeyboardInterrupt, EOFError):
            Client.block.set()
            _thread.interrupt_main()


class Cmd:

    "basic"

    @staticmethod
    def cmd(msg):
        "show commands."
        check = len(Commands.cmds) > len(Commands.names)
        msg.reply(",".join(sorted((check and Commands.cmds) or Commands.names)))

    @staticmethod
    def srv(msg):
        "generate systemd service file."
        import getpass
        name = getpass.getuser()
        msg.reply(SYSTEMD % (
            Main.name.upper(),
            name,
            name,
            name,
            Main.name
        ))

    @staticmethod
    def tbl(msg):
        "create table."
        core = {}
        md5s = {}
        Commands.names = {}
        if Main.mods:
            for name in Utils.spl(Main.mods):
                module = Mods.get(name, True)
                if not module:
                    continue
                if not module.__file__:
                    continue
                md5s[name] = MD5.md5(module.__file__)
                for cmd in Commands.scan(module):
                    Commands.names[Methods.getname(cmd)] = cmd.__module__.split(".")[-1]
        corepath = d(str(inspect.getsourcefile(Mods)))
        MD5.createmd5(corepath, core)
        msg.reply("# This file is placed in the Public Domain.")
        msg.reply("\n")
        msg.reply('"tables"')
        msg.reply("\n")
        msg.reply(f"CORE = {JSON.dumps(core, indent=4, sort_keys=True)}")
        msg.reply("\n")
        msg.reply(f"MODULES = {JSON.dumps(md5s, indent=4, sort_keys=True)}")
        msg.reply("\n")
        msg.reply(f"NAMES = {JSON.dumps(Commands.names, indent=4, sort_keys=True)}")
        msg.reply("\n")
        msg.reply("def __dir__():")
        msg.reply("    return (")
        msg.reply("        'CORE',")
        msg.reply("        'MODULES',")
        msg.reply("        'NAMES'")
        msg.reply("    )")

    @staticmethod
    def ver(msg):
        "show verson."
        msg.reply(f"{Main.name.upper()} {MD5.coremd5}")


SYSTEMD = """[Unit]
Description=%s
After=multi-user.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%s -s

[Install]
WantedBy=multi-user.target"""


def __dir__():
    return (
        'Boot',
        'Cmd'
    )
