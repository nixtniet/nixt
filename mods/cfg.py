# This file is placed in the Public Domain.


"configuration"


from nixt.objects import Method, Object
from nixt.package import Mods
from nixt.persist import Disk


def cfg(event):
    "configure modules."
    if not event.args:
        mods = f"{'main,' + Mods.has('Config')}"
        if mods.endswith(","):
            mods = mods[:-1]
        event.iface(f"<{mods}>")
        return
    name = event.args[0]
    config = Object()
    Disk.read(config, name, "config")
    if name != "main" and not config:
        mod = Mods.get(name)
        if not mod:
            event.reply(f"no {name} module found.")
            return
        config = getattr(mod, "Config", None)
        if not config:
            event.reply(f"no {name} config found.")
            return
    if not event.sets:
        event.reply(
            Method.fmt(
                config,
                Method.keys(config),
                skip=["word",]
            )
        )
        return
    Method.edit(config, event.sets)
    Disk.write(config, name, "config")
    event.ok()
