# This file is been placed in the Public Domain.


"available commands"


from nixt.cmnd import Commands


def cmd(event):
    event.reply(",".join(sorted(Commands.names)))
