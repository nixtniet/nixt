# This file is placed in the Public Domain.


"main"


import logging
import os
import sys
import threading
import time
import _thread


from .defines import Client, Cmd, Commands, Logging, Main, Message, Output
from .defines import Md5, Mods, Parse, Task, Thread, Utils, Workdir


class Kernel:

    command = Commands.command
    parse = Parse.parse
    pid = Workdir.pid
    scanner = Mods.scanner

    @classmethod
    def banner(cls):
        "hello."
        tmr = time.ctime(time.time()).replace("  ", " ")
        txt = "%s since %s %s (%s)" % (
            Main.name.upper(),
            tmr,
            Main.sets.level.upper() or "WARNING",
            Md5.core()
        )
        return txt.replace("  ", " ")

    @classmethod
    def configure(cls):
        "configure program."
        Workdir.wdr = Workdir.wdr or Workdir.home(Main.name)
        Workdir.skel()
        Mods.dir("modules", Workdir.moddir())
        Logging.size(len(Main.name))
        Logging.level(Main.sets.level or "warning")
        Mods.sums()
        Md5.check(Mods.core)

    @classmethod
    def daemon(cls):
        "run in the background."
        pid = os.fork()
        if pid != 0:
            os._exit(0)
        os.setsid()
        pid2 = os.fork()
        if pid2 != 0:
            os._exit(0)
        if not Main.sets.verbose:
            cls.null(sys.stdin)
            cls.null(sys.stdout)
            cls.null(sys.stderr)
        os.umask(0)
        if not Main.nochdir:
            os.chdir("/")
        os.nice(10)

    @classmethod
    def forever(cls):
        "run forever until ctrl-c."
        while True:
            try:
                time.sleep(1.0)
            except (KeyboardInterrupt, EOFError):
                break

    @classmethod
    def init(cls):
        "call init of modules that have an init function."
        thrs = []
        for name in Utils.spl(Main.sets.mods or Main.sets.default):
            mod = Mods.get(name)
            if not mod or "init" not in dir(mod):
                continue
            thrs.append(Thread.launch(mod.init))
        if thrs and Main.sets.wait:
            for thr in thrs:
                try:
                    thr.join()
                except (KeyboardInterrupt, EOFError):
                    return False
        return True

    @classmethod
    def null(cls, io):
        "route to dev/null."
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), io.fileno())

    @classmethod
    def privileges(cls):
        "drop privileges."
        import getpass
        import pwd
        pwnam2 = pwd.getpwnam(getpass.getuser())
        os.setgid(pwnam2.pw_gid)
        os.setuid(pwnam2.pw_uid)

    @classmethod
    def wait(cls, nr=1):
        "wait until nr threads left running."
        while 1:
            if len(threading.enumerate()) == nr:
                break
            time.sleep(0.01)

    @classmethod
    def wrap(cls, func, *args, dofinal=None):
        "restore console."
        import termios
        try:
            old = termios.tcgetattr(sys.stdin.fileno())
        except termios.error:
            old = False
        Kernel.wrapped(func, *args)
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)
        if dofinal:
            dofinal()

    @classmethod
    def wrapped(cls, func, *args):
        "wrap function in a try/except, silence ctrl-c/ctrl-d."
        try:
            func(*args)
        except (KeyboardInterrupt, EOFError):
            Output.block.set()
            Task.block.set()
            _thread.interrupt_main()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


class CLI(Client):

    def raw(self, text):
        "output to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))


class Scripts:

    @staticmethod
    def daemon():
        "background script."
        Kernel.parse(Main, " ".join(sys.argv[1:]))
        print(Main.sets)
        if not Main.sets.service:
            Kernel.daemon()
        Kernel.privileges()
        Kernel.configure()
        Kernel.pid(Main.name)
        if Main.sets.verbose:
            Kernel.banner()
        Kernel.scanner()
        Kernel.init()
        Kernel.forever()

    @staticmethod
    def control():
        "cli script."
        Kernel.parse(Main, " ".join(sys.argv[1:]))
        Kernel.configure()
        Kernel.scanner()
        cli = CLI()
        cli.silent = False
        evt = Message()
        evt.orig = repr(cli)
        evt.text = Main.otxt
        Commands.add(Cmd.cmd)
        Kernel.command(evt)


def main():
    Kernel.wrapped(Scripts.control)


if __name__ == "__main__":
    main()
