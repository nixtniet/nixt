# This file is placed in the Public Domain.


import os
import shutil


from nixt.classes import Mods, Workdir


def cpy(event):
    path = os.path.join(
                        Mods.path.rsplit("nixt")[-3],
                        "nixt",
                        "share",
                        "nixt",
                        "examples"
                       ) 
    event.reply(f"using {path}")
    shutil.copytree(path, Workdir.moddir(), dirs_exist_ok=True)
    event.reply("done")
