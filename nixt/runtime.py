# This file is placed in the Public Domain.


"main"


import os
import sys


from .defines import Boot, Client, Cmd, Commands, Main, Message
from .defines import Workdir


class Kernel(Boot):

    pid = Workdir.pid

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
