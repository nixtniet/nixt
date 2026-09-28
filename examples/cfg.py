# This file is placed in the Public Domain.


"configuration"


from typing import Union


from nixt.defines import Data, Disk, Method, Mods


def cfg(message):
    "configure modules."
    if not message.args:
        mods = f"{'main,' + Mods.has('Config')}"
        mods = mods.removesuffix(mods)
        message.iface(f"<{mods}>")
        return
    name = message.args[0]
    config: Union[Data, None] = Data()
    Disk.read(config, name, "config")
    if name != "main" and not config:
        mod = Mods.get(name)
        if not mod:
            message.reply(f"no {name} module found.")
            return
        config = getattr(mod, "Config", None)
        if not config:
            message.reply(f"no {name} config found.")
            return
    if not message.sets:
        message.reply(
            Method.fmt(
                config,
                Method.keys(config),
                skip=["word",]
            )
        )
        return
    Method.edit(config, message.sets)
    Disk.write(config, name, "config")
    message.ok()
