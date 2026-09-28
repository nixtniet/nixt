# This file is placed in the Public Domain.


"show version"


from nixt.defines import Main, MD5


def ver(message):
    "show verson."
    message.reply(f"{Main.name.upper()} {MD5.core()}")
