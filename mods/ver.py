# This file is placed in the Public Domain.


"show version"


from nixt.defines import Main, Md5


def ver(cls, event):
    "show verson."
    event.reply(f"{Main.name.upper()} {Md5.core()}")
