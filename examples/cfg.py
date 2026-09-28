# This file is placed in the Public Domain.


"configuration"


from typing import Union


from nixt.defines import Data, Disk, Method, Mods


def cfg(msg):
    "configure modules."
    if not msg.args:
        mods = f"{'main,' + Mods.has('Config')}"
        mods = mods.removesuffix(mods)
        msg.iface(f"<{mods}>")
        return
    name = msg.args[0]
    config: Union[Data, None] = Data()
    Disk.read(config, name, "config")
    if name != "main" and not config:
        mod = Mods.get(name)
        if not mod:
            msg.reply(f"no {name} module found.")
            return
        config = getattr(mod, "Config", None)
        if not config:
            msg.reply(f"no {name} config found.")
            return
    if not msg.sets:
        msg.reply(
            Method.fmt(
                config,
                Method.keys(config),
                skip=["word",]
            )
        )
        return
    Method.edit(config, msg.sets)
    Disk.write(config, name, "config")
    msg.ok()
