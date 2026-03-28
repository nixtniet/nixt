# This file is placed in the Public DOmain.


"kernel"


from nixt.kernels import Kernel
from nixt.objects import Methods


def krn(event):
    "dump kernel to disk."
    event.reply(Methods.fmt(Kernel))
