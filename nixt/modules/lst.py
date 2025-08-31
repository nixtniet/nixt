# This file is been placed in the Public Domain.


"available types"


from ..persist import Workdir


def ls(event):
    event.reply(",".join([x.split(".")[-1].lower() for x in Workdir.types()]))
