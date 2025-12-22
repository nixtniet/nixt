# This file is placed in the Public Domain.


import os


from nixt.configs import Config
from nixt.utility import where


def pth(event):
    fn = where(Config)
    path = os.path.join(fn, 'network', 'html', "index.html")
    event.reply(f"file://{path}")
