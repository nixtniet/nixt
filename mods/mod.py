# This file is placed in the Public Domain.


"available modules"


import os


def mod(event):
    path = os.path.dirname(__file__)
    mods = []
    for mdd in os.listdir(path):
        if mdd in ["command.py", "names.py", "face.py"]:
            continue
        if mdd.startswith("__"):
            continue
        if mdd.endswith("~"):
            continue
        mods.append(mdd[:-3])
    event.reply(",".join(sorted(mods)))
